# Research Wiki

Research Wiki is a deployment-neutral public reference for building evidence-first research agents. It publishes reusable skills, portable MCP/client source files, setup guidance, and documentation for grounded research workflows. It does not include a hosted MCP server, credentials, or a directly installable vendor plugin.

## Start here

- [Quick start](guides/quickstart.md)
- [MCP setup](guides/mcp-setup.md)
- [Agent workflows](guides/agent-workflows.md)
- [Plugin installation](guides/plugin-installation.md)
- [Skills catalog](skills/index.md)
- [Documentation](docs/index.md)

## Agent access

- Documentation index: [`llms.txt`](llms.txt)
- Complete copy-ready context: [`llms-full.txt`](llms-full.txt)
- Canonical skills: [`skills/`](skills/)
- Setup skill: [`skills/setup-and-discovery/SKILL.md`](skills/setup-and-discovery/SKILL.md)
- Setup schema: [`skills/setup-and-discovery/schema.json`](skills/setup-and-discovery/schema.json)

Give an agent the deployed `llms.txt` URL for selective retrieval. The documentation UI also provides **Copy all for agent** for the complete public context.

## Principles

1. Authorization runs before retrieval.
2. Exact claims require exact evidence.
3. Every material claim keeps a citation.
4. Generated summaries are projections, not source authority.
5. Missing or conflicting evidence produces a limitation, not a guess.

## Local validation

```bash
python3 scripts/validate_public.py
```

The public source and validator are dependency-free. GitHub Pages builds the Markdown after validation; the workflow is the reproducible build contract. After deployment, verify the rendered routes with:

```bash
python3 scripts/validate_public.py --site-url https://kitkitkittt.github.io/research-wiki/
python3 scripts/validate_public.py --public-alias-url https://research.vnibb.xyz/
```

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Public content must use placeholders for hosts and credentials and must contain no private deployment details, customer data, machine paths, or generated secrets.
