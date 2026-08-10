from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "_site", "vendor", "__pycache__"}
FORBIDDEN = {
    "Windows drive path": re.compile(r"\b[A-Za-z]:[\\/]"),
    "private environment path": re.compile(r"/media/|/home/[^<\s]+/|/opt/[^<\s]+/"),
    "secret assignment": re.compile(
        r"(?i)(?:api[_-]?key|token|secret|password)\s*[=:]\s*(?![<{][$]?).{8,}"
    ),
}
ALLOWED_PUBLIC_TOKEN_SHA256 = {
    "9b04b2f1f6921bc4866c138a6c93d74973b65f04bf961ec2fa5a5e6da2133725",
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
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_LINK = re.compile(r"\b(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
LIQUID_LINK = re.compile(r"\{\{\s*['\"]([^'\"]+)['\"]\s*\|\s*relative_url\s*\}\}")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
EXPLICIT_ANCHOR = re.compile(r"\{#([a-z0-9_-]+)\}")
HTML_ANCHOR = re.compile(r"\bid=[\"']([a-zA-Z0-9_-]+)[\"']")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
SKILL_NAMES = tuple(
    path.parent.name for path in sorted(ROOT.glob("skills/*/SKILL.md"))
)
AGENT_SOURCE_PATHS = (
    *(path.relative_to(ROOT) for path in sorted((ROOT / "docs").glob("*.md"))),
    *(path.relative_to(ROOT) for path in sorted((ROOT / "guides").glob("*.md"))),
    Path("skills/index.md"),
    Path("skills/reference.md"),
    *(Path("skills") / name / "SKILL.md" for name in SKILL_NAMES),
    *(path.relative_to(ROOT) for path in sorted((ROOT / "skills").glob("*/schema.json"))),
    Path("plugins/index.md"),
    Path("plugins/research-wiki-agent/index.md"),
    Path("plugins/research-wiki-agent/plugin.json"),
    Path("plugins/research-wiki-agent/mcp.json"),
)
AGENT_INDEX_ENTRIES = (
    ("Documentation overview", "docs/"),
    ("Setup and discovery", "docs/setup-and-discovery/"),
    ("Evidence model", "docs/how-evidence-works/"),
    ("Authority and access", "docs/authority-and-access/"),
    ("Search and citations", "docs/search-and-citations/"),
    ("Versioning and conflicts", "docs/versioning-and-conflicts/"),
    ("Table safety", "docs/table-safety/"),
    ("Security model", "docs/security-model/"),
    ("MCP design guidance", "docs/mcp-tool-contract/"),
    ("Portable agent template", "docs/agent-plugin-contract/"),
    ("Glossary", "docs/glossary/"),
    ("Guides", "guides/"),
    ("Skill reference", "skills/reference/"),
    ("Full public context", "llms-full.txt"),
)
DEPLOYED_ROUTES = (
    "./",
    "guides/",
    "guides/quickstart/",
    "guides/mcp-setup/",
    "skills/",
    "skills/reference/",
    "docs/setup-and-discovery/",
    "plugins/",
    "plugins/research-wiki-agent/",
    "docs/",
    "security/",
    "contributing/",
    "404.html",
)
DEPLOYED_AGENT_FILES = ("llms.txt", "llms-full.txt")
PUBLIC_ALIAS_ROUTES = tuple(
    route for route in DEPLOYED_ROUTES if route not in {"./", "404.html"}
)
DEPLOYED_SKILL_FILES = tuple(
    (f"skills/{name}/SKILL.md", Path("skills") / name / "SKILL.md")
    for name in SKILL_NAMES
) + tuple(
    (f"skills/{path.parent.name}/schema.json", path.relative_to(ROOT))
    for path in sorted((ROOT / "skills").glob("*/schema.json"))
)
DEPLOYED_DOWNLOADS = tuple(
    (f"downloads/skills/{name}/SKILL.md", Path("skills") / name / "SKILL.md")
    for name in SKILL_NAMES
)
PUBLIC_ALIAS_FILES = (
    *(
        (route, source, "application/json" if source.suffix == ".json" else "text/markdown")
        for route, source in DEPLOYED_SKILL_FILES
        if source.parts[:2] == ("skills", "setup-and-discovery")
    ),
    *((route, source, "text/markdown") for route, source in DEPLOYED_DOWNLOADS),
    *((route, Path(route), "text/plain") for route in DEPLOYED_AGENT_FILES),
)


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
        "access_token",
        "api_key",
        "apikey",
        "authorization",
        "bearer_token",
        "client_secret",
        "password",
        "private_key",
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
                and child.strip() != "<your-token>"
                and re.fullmatch(r"\$\{[A-Z][A-Z0-9_]*\}", child.strip()) is None
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
            if (
                (digest := hashlib.sha256(token.encode()).hexdigest())
                in FORBIDDEN_TOKEN_SHA256
                and digest not in ALLOWED_PUBLIC_TOKEN_SHA256
            )
        ]
        if forbidden_tokens:
            errors.append(
                f"internal name: {path.relative_to(ROOT)}"
            )


def validate_scanner_policy(errors: list[str]) -> None:
    forbidden_brand = hashlib.sha256(bytes((118, 99, 105))).hexdigest()
    if forbidden_brand not in FORBIDDEN_TOKEN_SHA256:
        errors.append("forbidden brand scanner policy missing")
    if forbidden_brand in ALLOWED_PUBLIC_TOKEN_SHA256:
        errors.append("forbidden brand scanner policy allowlisted")


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


def target_source(target: Path) -> Path | None:
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return None
    try:
        relative = target.relative_to((ROOT / "downloads" / "skills").resolve())
        if relative.parts[-1:] == ("SKILL.md",) and len(relative.parts) == 2:
            canonical = ROOT / "skills" / relative.parts[0] / "SKILL.md"
            if canonical.is_file():
                return canonical
    except ValueError:
        pass
    if target.exists() and target.is_file():
        return target
    if target.suffix:
        return None
    if target.with_suffix(".md").is_file():
        return target.with_suffix(".md")
    if (target / "index.md").is_file():
        return target / "index.md"
    return None


def target_exists(target: Path) -> bool:
    if target.exists() and target.is_dir():
        try:
            target.relative_to(ROOT.resolve())
            return True
        except ValueError:
            return False
    return target_source(target) is not None


def heading_anchor(value: str) -> str:
    value = re.sub(r"\s*\{#[^}]+\}\s*$", "", value).strip().casefold()
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    values = set(EXPLICIT_ANCHOR.findall(text))
    values.update(HTML_ANCHOR.findall(text))
    values.update(anchor for heading in HEADING.findall(text) if (anchor := heading_anchor(heading)))
    return values


def validate_links(errors: list[str]) -> None:
    for path in files():
        if path.suffix not in {".md", ".html"}:
            continue
        text = path.read_text(encoding="utf-8")
        links = {raw for raw in MARKDOWN_LINK.findall(text) if "{{" not in raw}
        links.update(raw for raw in HTML_LINK.findall(text) if "{{" not in raw)
        links.update(LIQUID_LINK.findall(text))
        for raw in sorted(links):
            target = link_target(path, raw)
            if target is not None and not target_exists(target):
                errors.append(f"broken link: {path.relative_to(ROOT)} -> {raw}")
                continue
            parsed = urlsplit(unquote(raw.strip().strip("<>")))
            if not parsed.fragment:
                continue
            source = target_source(target) if target is not None else path
            if source is not None and parsed.fragment not in anchors(source):
                errors.append(f"broken anchor: {path.relative_to(ROOT)} -> {raw}")


def validate_plugin_contract(errors: list[str]) -> None:
    root = ROOT / "plugins" / "research-wiki-agent"
    plugin_path = root / "plugin.json"
    mcp_path = root / "mcp.json"
    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
    except OSError as exc:
        errors.append(f"required plugin artifact unavailable: {exc.filename}")
        return
    except json.JSONDecodeError:
        return
    required_plugin = {
        "schemaVersion": "1.0",
        "name": "research-wiki-agent",
        "packageType": "portable-source-template",
        "directInstall": False,
        "mcp": "mcp.json",
        "skills": "skills",
    }
    if any(plugin.get(key) != value for key, value in required_plugin.items()):
        errors.append("plugin manifest does not match the public template contract")
    if not isinstance(plugin.get("version"), str) or not plugin["version"].strip():
        errors.append("plugin manifest requires a version")
    server = mcp.get("mcpServers", {}).get("research-wiki", {})
    if server != {
        "type": "streamable-http",
        "url": "https://<your-host>/mcp/",
    }:
        errors.append("MCP template does not match the public placeholder contract")
    for field in ("mcp", "skills"):
        target = root / str(plugin.get(field, ""))
        if not target_exists(target.resolve()):
            errors.append(f"plugin artifact missing: {field}")


def validate_plugin_parity(errors: list[str]) -> None:
    plugin = ROOT / "plugins" / "research-wiki-agent" / "skills"
    canonical_skills = {
        path.parent.name: path for path in sorted(ROOT.glob("skills/*/SKILL.md"))
    }
    bundled_skills = {
        path.parent.name: path for path in sorted(plugin.glob("*/SKILL.md"))
    }
    if canonical_skills.keys() != bundled_skills.keys():
        errors.append("canonical and bundled skill membership differ")
    for name, canonical in canonical_skills.items():
        bundled = bundled_skills.get(name)
        if bundled is not None and canonical.read_bytes() != bundled.read_bytes():
            errors.append(f"plugin skill drift: {name}")
    for canonical in sorted(ROOT.glob("skills/*/schema.json")):
        bundled = plugin / canonical.parent.name / "schema.json"
        if not bundled.is_file():
            errors.append(f"plugin skill schema missing: {canonical.parent.name}")
        elif canonical.read_bytes() != bundled.read_bytes():
            errors.append(f"plugin skill schema drift: {canonical.parent.name}")


def public_site_url() -> str:
    values: dict[str, str] = {}
    for line in (ROOT / "_config.yml").read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition(":")
        if separator and key in {"url", "baseurl", "public_url"}:
            values[key] = value.strip().strip("'\"")
    if values.get("public_url"):
        return values["public_url"].rstrip("/") + "/"
    if not values.get("url"):
        raise ValueError("_config.yml requires url for agent artifacts")
    return values["url"].rstrip("/") + "/" + values.get("baseurl", "").strip("/") + "/"


def without_front_matter(text: str) -> str:
    match = FRONT_MATTER.match(text)
    return text[match.end():].strip() if match else text.strip()


def agent_link(source: Path, raw: str, base: str) -> str:
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc or raw.startswith(("#", "mailto:")):
        return raw
    target = (source.parent / parsed.path).resolve()
    try:
        relative = target.relative_to(ROOT.resolve())
    except ValueError:
        return raw
    if relative.parts[-1:] == ("SKILL.md",) and len(relative.parts) >= 3:
        route = f"downloads/skills/{relative.parts[-2]}/SKILL.md"
    elif relative.name == "index.md":
        route = relative.parent.as_posix().rstrip("/") + "/"
    elif relative.suffix == ".md":
        route = relative.with_suffix("").as_posix().rstrip("/") + "/"
    else:
        route = relative.as_posix()
    absolute = urljoin(base, route)
    return absolute + (f"#{parsed.fragment}" if parsed.fragment else "")


def agent_source_text(source: Path, base: str) -> str:
    body = without_front_matter(source.read_text(encoding="utf-8"))
    if source.suffix == ".json":
        return f"```json\n{body}\n```"
    body = LIQUID_LINK.sub(
        lambda match: urljoin(base, match.group(1).lstrip("/")),
        body,
    )
    return MARKDOWN_LINK.sub(
        lambda match: match.group(0).replace(
            match.group(1), agent_link(source, match.group(1), base)
        ),
        body,
    )


def agent_artifacts() -> dict[str, str]:
    base = public_site_url()
    index_lines = [
        "# Research Wiki",
        "",
        "> Deployment-neutral public documentation for evidence-first research agents.",
        "",
        "Use this index to retrieve only the context needed for a task. This repository does not host an MCP server or credentials.",
        "",
        "## Documentation",
        "",
    ]
    index_lines.extend(
        f"- [{label}]({urljoin(base, route)})" for label, route in AGENT_INDEX_ENTRIES
    )
    index_lines.extend(
        [
            "",
            "## Canonical skills",
            "",
            *(
                f"- [{name}]({urljoin(base, f'downloads/skills/{name}/SKILL.md')})"
                for name in SKILL_NAMES
            ),
            "",
        ]
    )
    full_lines = [
        "# Research Wiki — full public agent context",
        "",
        f"Source: {urljoin(base, 'llms.txt')}",
        "Boundary: public reference material only; no credentials, private evidence, live endpoint, or deployment authority.",
        "",
    ]
    for relative in AGENT_SOURCE_PATHS:
        source = ROOT / relative
        full_lines.extend(
            [
                "---",
                f"Source file: {relative.as_posix()}",
                "---",
                "",
                agent_source_text(source, base),
                "",
            ]
        )
    return {
        "llms.txt": "\n".join(index_lines),
        "llms-full.txt": "\n".join(full_lines),
    }


def write_agent_artifacts() -> None:
    for name, content in agent_artifacts().items():
        (ROOT / name).write_text(content, encoding="utf-8")


def validate_agent_artifacts(errors: list[str]) -> None:
    for name, expected in agent_artifacts().items():
        path = ROOT / name
        try:
            observed = path.read_text(encoding="utf-8")
        except OSError:
            errors.append(f"agent artifact missing: {name}")
            continue
        if observed != expected:
            errors.append(f"agent artifact drift: {name}")


def export_skill_downloads(destination: Path) -> None:
    root = destination.resolve()
    if root == ROOT.resolve() or root == (ROOT / "skills").resolve():
        raise ValueError("download export cannot overwrite canonical skills")
    for name in SKILL_NAMES:
        source = ROOT / "skills" / name / "SKILL.md"
        for target in (
            root / "downloads" / "skills" / name / "SKILL.md",
            root / "skills" / name / "SKILL.md",
        ):
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source in sorted((ROOT / "skills").glob("*/schema.json")):
        target = root / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def validate_deployed_site(site_url: str, errors: list[str]) -> None:
    base = site_url.rstrip("/") + "/"
    for route in DEPLOYED_ROUTES:
        url = urljoin(base, route)
        last_error = ""
        for attempt in range(6):
            try:
                request = Request(url, headers={"User-Agent": "research-wiki-validator"})
                with urlopen(request, timeout=20) as response:
                    content_type = response.headers.get_content_type()
                    body = response.read(16_384).lower()
                    expected_path = urlsplit(url).path.rstrip("/")
                    final_path = urlsplit(response.geturl()).path.rstrip("/")
                    if (
                        response.status == 200
                        and content_type == "text/html"
                        and final_path == expected_path
                        and b'<main id="content"' in body
                    ):
                        break
                    last_error = (
                        f"HTTP {response.status} {content_type} at {response.geturl()}"
                    )
            except (HTTPError, URLError, TimeoutError) as exc:
                last_error = str(exc)
            if attempt < 5:
                time.sleep(5)
        else:
            errors.append(f"deployed route failed: {url}: {last_error}")
    for route, source in DEPLOYED_SKILL_FILES + DEPLOYED_DOWNLOADS:
        url = urljoin(base, route)
        expected = (ROOT / source).read_bytes()
        try:
            request = Request(url, headers={"User-Agent": "research-wiki-validator"})
            with urlopen(request, timeout=20) as response:
                observed = response.read()
                if response.status != 200 or observed != expected:
                    errors.append(f"deployed skill file differs: {url}")
        except (HTTPError, URLError, TimeoutError) as exc:
            errors.append(f"deployed skill file failed: {url}: {exc}")
    for route in DEPLOYED_AGENT_FILES:
        url = urljoin(base, route)
        expected = (ROOT / route).read_bytes()
        try:
            request = Request(url, headers={"User-Agent": "research-wiki-validator"})
            with urlopen(request, timeout=20) as response:
                observed = response.read()
                if response.status != 200 or observed != expected:
                    errors.append(f"deployed agent artifact differs: {url}")
        except (HTTPError, URLError, TimeoutError) as exc:
            errors.append(f"deployed agent artifact failed: {url}: {exc}")
    missing_url = urljoin(base, "validator-missing-page")
    try:
        request = Request(missing_url, headers={"User-Agent": "research-wiki-validator"})
        with urlopen(request, timeout=20) as response:
            errors.append(
                f"deployed missing route returned HTTP {response.status}: {missing_url}"
            )
    except HTTPError as exc:
        body = exc.read(16_384).lower()
        if exc.code != 404 or b"page not found" not in body or b'<main id="content"' not in body:
            errors.append(f"custom 404 failed: {missing_url}: HTTP {exc.code}")
    except (URLError, TimeoutError) as exc:
        errors.append(f"custom 404 failed: {missing_url}: {exc}")


def validate_public_alias(site_url: str, errors: list[str]) -> None:
    base = site_url.rstrip("/") + "/"
    for route in PUBLIC_ALIAS_ROUTES:
        url = urljoin(base, route)
        last_error = ""
        for attempt in range(6):
            try:
                request = Request(url, headers={"User-Agent": "research-wiki-validator"})
                with urlopen(request, timeout=20) as response:
                    body = response.read(16_384).lower()
                    if (
                        response.status == 200
                        and response.headers.get_content_type() == "text/html"
                        and urlsplit(response.geturl()).path.rstrip("/") == urlsplit(url).path.rstrip("/")
                        and b'<main id="content"' in body
                    ):
                        break
                    last_error = f"HTTP {response.status} {response.headers.get_content_type()} at {response.geturl()}"
            except (HTTPError, URLError, TimeoutError) as exc:
                last_error = str(exc)
            if attempt < 5:
                time.sleep(5)
        else:
            errors.append(f"public alias route failed: {url}: {last_error}")
    for route, source, content_type in PUBLIC_ALIAS_FILES:
        url = urljoin(base, route)
        expected = (ROOT / source).read_bytes()
        last_error = ""
        for attempt in range(6):
            try:
                request = Request(url, headers={"User-Agent": "research-wiki-validator"})
                with urlopen(request, timeout=20) as response:
                    observed = response.read()
                    if (
                        response.status == 200
                        and response.headers.get_content_type() == content_type
                        and urlsplit(response.geturl()).path == urlsplit(url).path
                        and observed == expected
                    ):
                        break
                    last_error = f"HTTP {response.status} {response.headers.get_content_type()} at {response.geturl()}"
            except (HTTPError, URLError, TimeoutError) as exc:
                last_error = str(exc)
            if attempt < 5:
                time.sleep(5)
        else:
            errors.append(f"public alias file failed: {url}: {last_error}")
    asset_url = urljoin(base, "research-wiki/assets/styles.css")
    last_error = ""
    for attempt in range(6):
        try:
            request = Request(asset_url, headers={"User-Agent": "research-wiki-validator"})
            with urlopen(request, timeout=20) as response:
                if response.status == 200 and response.headers.get_content_type() == "text/css":
                    break
                last_error = f"HTTP {response.status} {response.headers.get_content_type()}"
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = str(exc)
        if attempt < 5:
            time.sleep(5)
    else:
        errors.append(f"public alias asset failed: {asset_url}: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-url")
    parser.add_argument("--public-alias-url")
    parser.add_argument("--export-downloads", type=Path)
    parser.add_argument("--write-agent-files", action="store_true")
    arguments = parser.parse_args()
    if arguments.write_agent_files:
        write_agent_artifacts()
    errors: list[str] = []
    validate_json(errors)
    validate_public_text(errors)
    validate_scanner_policy(errors)
    validate_front_matter(errors)
    validate_links(errors)
    validate_plugin_contract(errors)
    validate_plugin_parity(errors)
    validate_agent_artifacts(errors)
    if not errors and arguments.export_downloads:
        export_skill_downloads(arguments.export_downloads)
    if arguments.site_url:
        validate_deployed_site(arguments.site_url, errors)
    if arguments.public_alias_url:
        validate_public_alias(arguments.public_alias_url, errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"public validation passed: {len(files())} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
