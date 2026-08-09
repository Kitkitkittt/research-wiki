---
name: source-intake
description: Use when adding a new public or authorized document, checking rights and identity, monitoring processing, or submitting evidence for review.
---

# Source intake

## Workflow

1. **Declare rights** — record origin, confidentiality, allowed access lane, and authority expectations before content processing.
2. **Identify** — resolve entity, document family, reporting period, scope, language, and source location.
3. **Submit once** — use immutable bytes and one idempotency key. Do not replay an uncertain accepted submission.
4. **Observe** — monitor bounded processing without exposing credentials or source bodies in status logs.
5. **Validate** — require complete page coverage, source hashes, document identity, extraction QA, and citation-addressable output.
6. **Review** — route ambiguity, partial extraction, conflicting identity, and substantive reconstruction to human review.
7. **Publish** — make evidence searchable only after explicit policy, quality, authority, and current-version gates pass.

## Completion criterion

Complete only when the immutable source and its identity are recorded, every processing unit has a terminal disposition, and publication or withholding is explicit. An accepted-state-unknown submission remains quarantined without automatic replay.

## Related public references

- Authority and access
- Versioning and conflicts
