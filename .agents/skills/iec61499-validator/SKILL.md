---
name: iec61499-validator
description: Use this skill to validate IEC 61499 XML files (e.g. .fbt, .sub) for reserved keywords and Structured Text (ST) syntax compliance.
---

# Instructions for the Agent
## Prerequisites
- Python 3
- `lxml` (install with `python -m pip install lxml`)

When you create or edit IEC 61499 XML files (specifically block types like `.fbt`, `.sub`, `.adp`, `.dev`, `.res`, `.sys`), you must run this validator to ensure:
1. No reserved keywords (like `LEFT`, `RIGHT`, `MOD`, `AND`, etc.) are used as identifiers in the XML attributes (e.g. variable names, block names).
2. The Structured Text (ST) syntax inside `<ST>` elements is valid (correct assignment operators `:=`, proper semicolons, balanced blocks like `IF` / `END_IF`).

## Command to execute
Run the Python script in this folder from the terminal (requires `lxml`, install via `python -m pip install lxml`):
`python .agents/skills/iec61499-validator/validator.py <file.xml>`

## Error Handling
If the validator prints errors, check the line numbers and messages, adjust the XML file or ST code accordingly, and rerun the validator until it passes with `SUCCESS`.
