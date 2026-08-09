---
layout: default
title: Agent plugin contract
permalink: /docs/agent-plugin-contract/
---

# Agent plugin contract

An agent plugin is a portable package that points an AI client at a remote MCP server and supplies reusable skills.

## Package boundary

The package may contain:

- plugin metadata and semantic version;
- a placeholder MCP endpoint definition;
- skills and public schemas;
- integrity metadata generated for the package.

It contains no credentials, private hosts, source data, tenant settings, deployment state, or mutable cache.

## Compatibility

The plugin, MCP tool catalog, and skills form one compatibility set. A skill must not advertise a tool absent from the active catalog. A tool's required scope and input contract must match every generated reference.

## Installation responsibility

The deployment operator supplies endpoint and authentication details. The AI client supplies credentials. The plugin supplies process guidance. The MCP server remains the authority for access, readiness, tool behavior, and evidence.
