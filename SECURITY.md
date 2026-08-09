# Security policy

## Report a vulnerability

Use GitHub's private vulnerability reporting for this repository. Do not publish credentials, private endpoints, exploit details, customer data, or source documents in an issue.

## Public-content boundary

This repository contains documentation and templates, not live credentials or private evidence. Examples must use placeholders. Agent plugins must obtain authentication from the client or deployment environment rather than package files.

## Agent safety baseline

- Authorize before discovery or retrieval.
- Return neutral failures before authorization succeeds.
- Keep source evidence immutable.
- Treat generated content as non-authoritative.
- Re-fetch citations before displaying exact claims.
- Make partial success and uncertainty explicit.
- Require confirmation and idempotency for any future write-capable tool.
