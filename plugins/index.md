---
layout: default
title: Portable agent template
permalink: /plugins/
---

# Portable agent template

The [Research Wiki agent template](research-wiki-agent/) is a deployment-neutral directory of portable source files. It is not directly installable until a named client adapts the MCP and skill files through its supported custom-integration mechanisms.

## Included

- a versioned local file-contract manifest with `directInstall: false`;
- a remote MCP placeholder;
- all eight public research, evidence-integrity, source-intake, and working-project skills;
- no credentials or private deployment values.

Follow the [plugin installation guide](../guides/plugin-installation.md). The repository validator checks that bundled skills are byte-identical to the canonical skill directories.
