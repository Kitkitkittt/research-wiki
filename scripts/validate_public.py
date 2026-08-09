from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "_site", "vendor", "__pycache__"}
FORBIDDEN = {
    "Windows drive path": re.compile(r"\b[A-Za-z]:[\\/]"),
    "private environment path": re.compile(r"/media/|/home/[^<\s]+/|/opt/[^<\s]+/"),
    "secret assignment": re.compile(
        r"(?i)(?:api[_-]?key|token|secret|password)\s*[=:]\s*(?![<{][$]?).{8,}"
    ),
}
FORBIDDEN_TOKEN_SHA256 = {
    "985d577523f0aa08255b7673c8136cfd32237e76c189abf24d404953d658b601",
    "c2da6507fafc42afbf2baff0fc02ca5f1a183402a929479223cf96a840b1c929",
    "cd24c4c7fe961762d7af19fac679da024f68eff6db8e2a2b39ed88def73431cf",
    "2550116c1fecf2b3b81cd56548c20f77acc3f9540758d42bb88ea97fdd0590f4",
    "4db4749ec69acbadada46722f939e7a7068b61a76a500414f931c94f554cf018",
    "9b04b2f1f6921bc4866c138a6c93d74973b65f04bf961ec2fa5a5e6da2133725",
}
TOKEN = re.compile(r"[A-Za-z0-9.-]+")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not SKIP_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def secret_like(key: str) -> bool:
    normalized = key.casefold().replace("-", "_")
    return normalized in {
        "api_key",
        "apikey",
        "authorization",
        "password",
        "secret",
        "token",
    }


def inspect_json(value: object, path: Path, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if (
                secret_like(str(key))
                and isinstance(child, str)
                and child.strip()
                and "<your-token>" not in child
                and "${" not in child
            ):
                errors.append(f"secret-like JSON value: {path.relative_to(ROOT)}")
            inspect_json(child, path, errors)
    elif isinstance(value, list):
        for child in value:
            inspect_json(child, path, errors)


def validate_json(errors: list[str]) -> None:
    for path in files():
        if path.suffix == ".json":
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
                inspect_json(value, path, errors)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")


def validate_public_text(errors: list[str]) -> None:
    validator_path = Path(__file__).resolve()
    for path in files():
        if path.resolve() == validator_path:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in FORBIDDEN.items():
            match = pattern.search(text)
            if match:
                errors.append(
                    f"{label}: {path.relative_to(ROOT)}: {match.group(0)!r}"
                )
        forbidden_tokens = [
            token
            for token in TOKEN.findall(text.casefold())
            if hashlib.sha256(token.encode()).hexdigest()
            in FORBIDDEN_TOKEN_SHA256
        ]
        if forbidden_tokens:
            errors.append(
                f"internal name: {path.relative_to(ROOT)}"
            )


def validate_front_matter(errors: list[str]) -> None:
    for path in sorted(ROOT.glob("skills/*/SKILL.md")):
        match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
        if not match:
            errors.append(f"missing skill front matter: {path.relative_to(ROOT)}")
            continue
        fields: dict[str, str] = {}
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if not separator or key not in {"name", "description"} or not value:
                errors.append(f"invalid skill front matter: {path.relative_to(ROOT)}")
                break
            fields[key] = value
        missing = {"name", "description"} - set(fields)
        if missing:
            errors.append(
                f"skill front matter missing {sorted(missing)}: {path.relative_to(ROOT)}"
            )


def link_target(path: Path, raw: str) -> Path | None:
    raw = unquote(raw.strip().strip("<>"))
    if not raw or raw.startswith(("#", "mailto:")):
        return None
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc:
        return None
    target_text = parsed.path
    if not target_text:
        return None
    target = ROOT / target_text.lstrip("/") if target_text.startswith("/") else path.parent / target_text
    return target.resolve()


def target_exists(target: Path) -> bool:
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return False
    if target.exists():
        return True
    if target.suffix:
        return False
    return target.with_suffix(".md").exists() or (target / "index.md").exists()


def validate_links(errors: list[str]) -> None:
    for path in files():
        if path.suffix not in {".md", ".html"}:
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = link_target(path, raw)
            if target is not None and not target_exists(target):
                errors.append(f"broken link: {path.relative_to(ROOT)} -> {raw}")


def validate_plugin_parity(errors: list[str]) -> None:
    plugin = ROOT / "plugins" / "research-wiki-agent" / "skills"
    for canonical in sorted(ROOT.glob("skills/*/SKILL.md")):
        bundled = plugin / canonical.parent.name / "SKILL.md"
        if not bundled.exists():
            errors.append(f"plugin skill missing: {bundled.relative_to(ROOT)}")
        elif canonical.read_bytes() != bundled.read_bytes():
            errors.append(f"plugin skill drift: {canonical.parent.name}")


def main() -> int:
    errors: list[str] = []
    validate_json(errors)
    validate_public_text(errors)
    validate_front_matter(errors)
    validate_links(errors)
    validate_plugin_parity(errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"public validation passed: {len(files())} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
