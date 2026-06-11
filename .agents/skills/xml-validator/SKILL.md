---
name: xml-validator
description: Use this skill when XML files need to be edited, created, or validated against an XSD schema.
---

# Instructions for the Agent
When you touch XML files, you must mandatory ensure validation.

## Command to execute
Run the Python script in this folder from the terminal:
`python .agents/skills/xml-validator/validate.py <file.xml> <schema.xsd_or_dtd>`

## Error Handling
If the script fails, read the terminal output (stdout/stderr), adjust the XML file to the schema specifications, and run the script again until it passes without errors.
