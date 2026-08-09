---
layout: default
title: Research Wiki agent plugin
permalink: /plugins/research-wiki-agent/
---

# Research Wiki agent plugin

This directory is a portable **template**, not a client-vendor package. Its contract is intentionally small:

- `plugin.json` identifies the package version and relative artifact locations;
- `mcp.json` supplies a remote Streamable HTTP placeholder;
- `skills/*/SKILL.md` contains canonical agent process guidance;
- authentication remains in the client or deployment environment.

## Install

1. Copy this directory to a temporary configuration workspace.
2. Replace the placeholder MCP URL in `mcp.json`.
3. Import the MCP JSON and skill directories using your client's documented custom-MCP and custom-skill mechanisms.
4. If a client requires another manifest shape, adapt `plugin.json` at the client boundary while preserving `mcp.json` and the skill bytes.

No universal plugin-install format exists across AI clients. The public package documents its own file contract rather than claiming compatibility with an unnamed client.
