---
layout: default
title: Portable template adaptation
permalink: /guides/plugin-installation/
---

# Portable template adaptation

The public template bundles agent guidance and a placeholder MCP definition. It does not contain credentials, private hosts, source documents, deployment state, or a vendor manifest. It is not directly installable: copy its MCP and skill source files through the documented custom-integration mechanisms of a named client.

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

1. Confirm that your named AI client supports custom remote MCP configuration and custom skill files. Stop if either mechanism is unavailable.
2. Copy [`plugins/research-wiki-agent`](../plugins/research-wiki-agent/) to a temporary workspace, not directly into a vendor plugin directory.
3. Replace `https://<your-host>/mcp/` in `mcp.json` with the endpoint supplied by your operator.
4. Import `mcp.json` through the client's custom MCP mechanism and each `skills/*/SKILL.md` through its custom skill mechanism.
5. Configure authentication in the AI client or deployment integration, not in the template files.
6. Start a new conversation and ask the client to list available Research Wiki tools and describe the evidence-first workflow.

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
