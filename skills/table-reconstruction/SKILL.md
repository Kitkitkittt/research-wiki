---
name: table-reconstruction
description: Use when financial or research tables are split across pages, repeated as fragments, or need a cited long-form and pivoted presentation.
---

# Table reconstruction

## Workflow

1. **Collect** — load every physical fragment with document, page, table, cell, and citation identity.
2. **Preserve** — retain raw cell strings, row and column spans, headers, units, periods, and source order.
3. **Propose** — identify possible continuations using adjacency, explicit continuation labels, repeated headers, and compatible geometry.
4. **Validate** — require matching document, logical table, columns, spans, units, periods, scope, and total behavior.
5. **Separate** — keep incompatible or ambiguous fragments distinct and assign a review state.
6. **Project** — build long-form observations from validated source cells. A pivoted table or chart resolves values from those observations rather than model output.
7. **Cite** — attach source-cell citations to every displayed value and expose physical fragments for inspection.

## Guardrails

Never pad, truncate, reorder, infer, or generate cells to make a table rectangular. Never treat embedding similarity or a model-proposed join as verified structure. Charts remain supplementary to an accessible cited table.

## Completion criterion

Complete only when every joined fragment passes deterministic compatibility checks and every displayed value maps to source cells. Otherwise return separate cited fragments with a review limitation.

## Related public references

- Multi-page table safety
- How evidence works
