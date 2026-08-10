---
layout: default
title: Documentation
permalink: /docs/
description: Technical reference for evidence authority, retrieval, citations, safety, and agent integration.
---

# Documentation

Technical contracts and design guidance for evidence-first research systems. Analysts can read these pages directly; agents should start from [`llms.txt`]({{ '/llms.txt' | relative_url }}) or use **Copy all for agent** above for the full public context.

> **Agent handoff:** give an agent the documentation index URL shown in the handoff panel. It can fetch only the relevant pages, canonical skills, or full bundle from that index.

## Foundations

- [How evidence works](how-evidence-works.md)
- [Authority and access](authority-and-access.md)
- [Search, citations, and abstention](search-and-citations.md)

## Source integrity

- [Versioning and conflicts](versioning-and-conflicts.md)
- [Multi-page table safety](table-safety.md)
- [Security model](security-model.md)

## Integration

- [MCP tool design guidance](mcp-tool-contract.md)
- [Portable agent-template contract](agent-plugin-contract.md)
- [Glossary](glossary.md)
