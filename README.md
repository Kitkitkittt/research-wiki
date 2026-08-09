# Research Wiki

Research Wiki is a public reference for building evidence-first research agents. It publishes reusable skills, an agent-plugin template, MCP setup guidance, and documentation for grounded research workflows.

## Start here

- [Quick start](guides/quickstart.md)
- [MCP setup](guides/mcp-setup.md)
- [Agent workflows](guides/agent-workflows.md)
- [Plugin installation](guides/plugin-installation.md)
- [Skills catalog](skills/index.md)
- [Documentation](docs/index.md)

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

The public source and validator are dependency-free. GitHub Pages builds the Markdown with its maintained Jekyll action after validation; the workflow is the reproducible build contract.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Public content must use placeholders for hosts and credentials and must contain no private deployment details, customer data, machine paths, or generated secrets.
