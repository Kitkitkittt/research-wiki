---
layout: default
title: Setup and discovery
permalink: /docs/setup-and-discovery/
description: Connect to the hosted Research Wiki safely and discover only capabilities available to the current identity.
---

# Setup and discovery

Use the public documentation without authentication. Sign in to the workspace or configure an MCP client only when you need governed research capabilities.

## Entry points

| Surface | URL | Authentication |
| --- | --- | --- |
| Workspace | `https://research.vnibb.xyz/` | Required |
| Documentation | `https://research.vnibb.xyz/docs/` | Public |
| MCP | `https://research.vnibb.xyz/mcp/research-brain/` | Required |
| Setup skill | `https://research.vnibb.xyz/skills/setup-and-discovery/SKILL.md` | Public |
| Setup schema | `https://research.vnibb.xyz/skills/setup-and-discovery/schema.json` | Public |

## Safe connection sequence

1. Open the workspace and authenticate with your assigned identity.
2. Keep credentials in the client or approved secret store.
3. Initialize the MCP session at the published endpoint.
4. Read the runtime capability matrix or call `system.describe_capabilities`.
5. List tools for the current identity.
6. Select only capabilities reported as ready and permitted.
7. Stop on typed authentication, permission, readiness, or scope errors.

## Agent setup

Give an agent the [setup skill]({{ '/skills/setup-and-discovery/SKILL.md' | relative_url }}) and its [machine schema]({{ '/skills/setup-and-discovery/schema.json' | relative_url }}). For broader context, use [`llms.txt`]({{ '/llms.txt' | relative_url }}) rather than copying unrelated documentation.

## Security boundary

Public skill and schema files describe behavior; they do not grant access. Never put a password, session cookie, bearer token, private source, or internal path into prompts, skill directories, repository files, or URLs.

Continue with [MCP setup]({{ '/guides/mcp-setup/' | relative_url }}) and [authority and access](authority-and-access.md).
