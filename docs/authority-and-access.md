---
layout: default
title: Authority and access
permalink: /docs/authority-and-access/
---

# Authority and access

Identity, authority, quality, and access answer different questions.

| Axis | Question |
| --- | --- |
| Identity | What logical document and version is this? |
| Authority | What review disposition does this evidence carry? |
| Quality | Which deterministic checks passed? |
| Access | May this caller retrieve it? |

No generic `approved` flag may replace all four.

## Permission-first retrieval

Authorization and hard scope filters run before lexical, dense, reranking, or model stages. Post-retrieval redaction is not a primary access control.

A safe order is:

```text
authentication
  -> authorization
  -> access lane
  -> entity
  -> period and family
  -> quality and authority
  -> current version
  -> candidate ranking
  -> citation re-fetch
```

If no authorized evidence remains, return an abstention. Do not broaden the scope or search restricted material to improve recall.

## Neutral failures

Before authorization succeeds, errors should reveal no restricted tool, document, entity, or capability detail. After authorization, typed limitations may explain missing, partial, stale, conflicting, or insufficient evidence without exposing internal diagnostics.
