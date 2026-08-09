---
layout: default
title: Security model
permalink: /docs/security-model/
---

# Security model

## Credentials

Keep credentials in the MCP client, an OAuth flow, or the deployment environment. Plugin packages, skills, prompts, logs, URLs, and public repositories contain no credential values.

## Tool discovery

Authenticate before starting the MCP session. Filter `tools/list` by the caller's effective scopes and capability readiness. Unauthorized callers receive neutral errors that reveal no hidden tool metadata.

## Evidence privacy

Apply access controls before ranking. Public telemetry should contain IDs, bounded counts, timings, states, and hashes—not query text, source text, document titles, paths, prompts, model reasoning, or provider payloads.

## Write-capable tools

Research tools should be read-only by default. A future write tool requires a distinct scope, explicit user confirmation, an idempotency key, immutable audit evidence, and a safe retry contract.

## Generated content

Treat model output as untrusted input. Validate tool arguments, citation IDs, table joins, formulas, URLs, renderer specifications, and exported files at the server boundary.
