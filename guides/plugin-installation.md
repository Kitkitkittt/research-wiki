---
layout: default
title: Plugin installation
permalink: /guides/plugin-installation/
---

# Plugin installation

The public plugin template bundles agent guidance and a placeholder MCP definition. It does not contain credentials, private hosts, source documents, or deployment state. It is a client-neutral file contract; import its MCP and skill files through the custom-integration mechanisms supported by your client.

## Package contents

```text
research-wiki-agent/
├── plugin.json
├── mcp.json
└── skills/
    ├── evidence-first-research/SKILL.md
    ├── company-research/SKILL.md
    ├── financial-analysis/SKILL.md
    ├── period-comparison/SKILL.md
    ├── citation-audit/SKILL.md
    ├── table-reconstruction/SKILL.md
    ├── source-intake/SKILL.md
    └── working-project/SKILL.md
```

## Configure

1. Copy [`plugins/research-wiki-agent`](../plugins/research-wiki-agent/) into the plugin location supported by your AI client.
2. Replace `https://<your-host>/mcp/` in `mcp.json` with the endpoint supplied by your operator.
3. Configure authentication in the AI client or deployment integration, not in the plugin files.
4. Enable the plugin for a new conversation.
5. Ask the client to list available Research Wiki tools and describe the evidence-first workflow.

## Verify

The installation is complete when:

- the client establishes one authenticated MCP session;
- tool discovery returns only authorized tools;
- the evidence-first research skill is available;
- a discovery request returns a source reference;
- opening the reference reproduces the cited evidence;
- no credential appears in the plugin directory.

## Updates

Treat the plugin version and its skills as one compatibility set. Re-run the repository validator after editing a skill so the bundled copies cannot drift.
