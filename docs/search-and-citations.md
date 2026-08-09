---
layout: default
title: Search, citations, and abstention
permalink: /docs/search-and-citations/
---

# Search, citations, and abstention

Search finds candidates. Citation fetch establishes the evidence a claim actually uses.

## Retrieval units

Good retrieval units preserve semantic boundaries:

- one complete section;
- one numbered note;
- one source table or governed table fragment;
- one page-backed passage;
- one structured observation with complete dimensions.

Do not split a numbered note, primary statement, or multi-page table at arbitrary token boundaries. A small child unit may retrieve quickly, but the agent should receive its cited parent context before interpretation.

## Citation closure

A material claim is closed when:

1. every cited ID resolves in the current authorized snapshot;
2. the fetched evidence supports that claim, not merely the topic;
3. numeric claims preserve source value, unit, scale, currency, period, and scope;
4. superseded and conflicting versions remain visible;
5. the answer can be regenerated from the recorded evidence set.

## Abstention

Abstain when evidence is absent, unauthorized, ambiguous, incomplete, stale, conflicting beyond resolution, or too weak for the requested answer class. Return the supported subset and explicit limitations only when the transport contract defines partial success.
