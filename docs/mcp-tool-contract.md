---
layout: default
title: MCP tool contract
permalink: /docs/mcp-tool-contract/
---

# MCP tool contract

This page is recommended design guidance for operators building an MCP service. This repository does not publish a live server or authoritative tool catalog. A deployment's own versioned catalog remains the source for server registration, client discovery, generated documentation, skills, and conformance tests.

## Tool fields

| Field | Purpose |
| --- | --- |
| `name` | Stable namespaced operation name |
| `description` | When the agent should call it |
| `inputSchema` | Closed, validated arguments |
| `outputSchema` | Typed success and limitation envelope |
| `requiredScope` | Authorization needed before discovery or call |
| `readiness` | Whether the backing capability can serve now |
| `compact` | Whether output is bounded for agent context |

## Error behavior

Distinguish transport, authentication, authorization, admission, evidence, cancellation, and internal failures. A zero count or empty authorized result is valid data, not automatically an error. Partial success must be explicit.

## Long-running research

Use durable operations for work that exceeds one tool call. Submission returns an operation ID; status and event tools provide progress; result tools return a typed terminal artifact. Cancellation and retries remain idempotent and authorization-bound.
