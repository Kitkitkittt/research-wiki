---
layout: default
title: Troubleshooting
permalink: /guides/troubleshooting/
---

# Troubleshooting

## The client cannot connect

- Confirm the host and path exactly match the operator-provided endpoint.
- Preserve the trailing slash when present.
- Confirm the client supports remote MCP over Streamable HTTP.
- Test DNS and TLS separately from MCP authentication.

## Authentication succeeds but tools are missing

Tool discovery is caller-specific. Confirm the credential carries the required scope and that the tool's backing capability is ready. A neutral missing-tool response should not reveal restricted tool names.

## Search returns no evidence

No evidence can mean the query is too broad, the requested period or family is absent, the source is outside the authorized lane, or the current version is withheld. Narrow the scope; do not remove permission or quality filters.

## An exact request abstains

Exact claims need verified structured evidence with matching entity, period, unit, scope, and current release. Use a cited narrative only when the request explicitly permits it. Never treat OCR text, embedding similarity, or model confidence as exact authority.

## A table looks incomplete

Open the source fragments. Page boundaries may split one logical table. Join fragments only when header, unit, period, geometry, and continuation evidence agree. Keep ambiguous fragments separate and mark them for review.

## A citation changed

Re-fetch the current citation. Source revisions, supersession, access changes, and release changes must fence cached or in-flight output. Historical results should remain bound to their frozen evidence snapshot.
