---
name: xml-validator
description: Use this skill when XML files need to be edited, created, or validated against an XSD schema.
---

# Instructions for the Agent
When you touch XML files, you must ensure they are validated.

## Prerequisites
- Python 3
- lxml (`python -m pip install lxml`)

## Commands to execute
### Single File Validation
Run the Python script in this folder from the terminal, specifying the XML file and the schema (.xsd or .dtd) (requires `lxml`, install via `python -m pip install lxml`):
`python .agents/skills/xml-validator/validate.py <file.xml> <schema.xsd/dtd>`

### Bulk Validation
To validate all blocks ("Bausteine") in the workspace directories (e.g., data libraries and test workspaces) against an auto-generated Clean-Room XSD (`fbt_clean.xsd`, no DTD is generated in bulk mode):
`python .agents/skills/xml-validator/validate.py --bulk`

## Error Handling
If the script fails, read the terminal output (stdout/stderr), adjust the XML file to the schema specifications, and run the validation again until it passes without errors.
