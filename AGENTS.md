# Agent instructions

Use this repository only for public Research Wiki documentation, reusable skills, plugin templates, and static-site assets.

For a bounded swarm task in this checkout, use [SWARM_READY.md](SWARM_READY.md) for source acceptance and the publication boundary. The public agent indexes serve readers of the wiki, not repository contributors.

Before editing:

1. Read `README.md` and the nearest guide or skill.
2. Keep examples deployment-neutral. Use `<your-host>` and `<your-token>` placeholders.
3. Keep credentials outside plugin and skill files.
4. Preserve the evidence-first rules in `docs/how-evidence-works.md`.
5. Run `python3 scripts/validate_public.py` after every content change.

A change is complete when every local link resolves, JSON and skill front matter parse, the public-content scan passes, and no generated `_site` output is committed.
