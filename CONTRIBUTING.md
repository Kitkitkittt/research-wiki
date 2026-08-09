# Contributing

## Content scope

Contributions may add or improve:

- public product and architecture documentation;
- MCP client setup and troubleshooting;
- reusable agent skills;
- deployment-neutral plugin templates;
- evidence, citation, table, versioning, and security guidance.

Use invented entities and placeholder hosts. Keep private infrastructure, customer data, proprietary corpus details, machine paths, credentials, operational receipts, and internal issue history outside this repository.

## Skill changes

Each skill must:

- use YAML front matter with `name` and `description`;
- state the trigger in its description;
- define an ordered workflow with checkable completion criteria;
- keep evidence retrieval separate from interpretation;
- specify abstention behavior;
- avoid real endpoints, credentials, and private identifiers.

## Validation

```bash
python3 scripts/validate_public.py
```

Open a pull request only after validation passes. Describe the user need, changed public interface, and any compatibility impact on plugin or skill consumers.
