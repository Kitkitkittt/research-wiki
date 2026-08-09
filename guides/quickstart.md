---
layout: default
title: Quick start
permalink: /guides/quickstart/
---

# Quick start

Research Wiki separates the research experience into three layers:

1. **Evidence** — immutable documents, exact passages, source cells, and structured observations.
2. **Research tools** — permission-first search, fetch, verify, compare, and long-running operations.
3. **Agent guidance** — skills that tell an AI client when to use each tool and when to abstain.

## The safe sequence

1. Resolve the entity and requested time period.
2. Select the requested answer class: exact fact, cited narrative, or discovery.
3. Discover tools only after authentication succeeds.
4. Apply access, scope, current-version, and quality filters before ranking evidence.
5. Search for candidates.
6. Fetch the exact cited passage, page, table cell, or structured observation.
7. Verify every material claim and displayed number.
8. Return limitations for missing, partial, ambiguous, superseded, or conflicting evidence.

## Pick the right interface

| Need | Interface |
| --- | --- |
| AI client or agent | MCP tools and bundled skills |
| Human documentation | This public site |
| Administration and operations | The deployment's authorized management surface |
| Internal specialist work | Server-side governed tool handlers, not recursive MCP sessions |

## Next step

Connect a client with the [MCP setup guide](mcp-setup.md), then install the [agent plugin](plugin-installation.md).
