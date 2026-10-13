---
layout: default
title: Research Wiki agent plugin
permalink: /plugins/research-wiki-agent/
---

# Research Wiki agent plugin

This directory contains portable **source files**, not a client-vendor package and not a direct-install artifact. Its local contract is intentionally small:

- `plugin.json` identifies the template version, `directInstall: false`, and relative artifact locations;
- `mcp.json` supplies a remote Streamable HTTP placeholder;
- `skills/*/SKILL.md` contains canonical agent process guidance;
- `skills/setup-and-discovery/schema.json` describes static capability/skill metadata and references separate REST and MCP discovery response contracts;
- authentication remains in the client or deployment environment.

## Install

1. Copy this directory to a temporary configuration workspace.
2. Replace the placeholder MCP URL in `mcp.json` with the absolute operator endpoint, preserving `/mcp/research-brain/` and the trailing slash.
3. Import source files through the client's documented custom mechanisms. For Codex, use the [manual TOML and environment-variable setup](../../guides/mcp-setup.md#manual-codex-setup), not generic JSON as Codex configuration.
4. Configure a deployment-issued API-key Bearer token in the client secret environment. This hosted setup does not imply OAuth provisioning or provider bootstrap.
5. If a client requires another manifest shape, adapt `plugin.json` at the client boundary while preserving the skill bytes.
6. Run authenticated discovery and one authorized search plus citation re-fetch. Discovery-only is connected, research blocked, not successful research integration.

No universal plugin-install format exists across AI clients. The public package documents its own file contract rather than claiming compatibility with an unnamed client.
