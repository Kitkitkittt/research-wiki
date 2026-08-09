---
layout: default
title: Multi-page table safety
permalink: /docs/table-safety/
---

# Multi-page table safety

Page-based extraction can split one logical table, repeat headers, omit continuation labels, or preserve cells in geometry that is not safely rectangular.

## Governed reconstruction

A model may propose which fragments belong together. Deterministic validation decides whether the proposal can be displayed as one table.

A safe join requires compatible:

- source document and logical table identity;
- adjacent or explicitly linked page sequence;
- column count and span geometry;
- repeated or continued headers;
- unit, currency, scale, period, and report scope;
- row-label continuation and total behavior;
- source-cell citations.

Preserve raw cell strings and physical fragment identities. Never pad, truncate, reorder, or invent cells to manufacture a rectangular table.

## Ambiguity

When geometry, period, unit, or continuation evidence is uncertain, render fragments separately with a review state. AI may explain the ambiguity, but it cannot convert a proposed join into verified structured fact.

## Presentation

A reconstructed table is a disposable projection. Every visible value maps to one or more source cells. Charts are supplementary and must retain the same cited table or accessible text representation.
