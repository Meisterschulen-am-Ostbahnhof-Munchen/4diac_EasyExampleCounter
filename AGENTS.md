# Agents & Skills

This document describes the available agents, subagents, and skills configured for this workspace.

## Available Skills

Skills are specialized instructions, scripts, and resources that extend the capabilities of the agent for specific tasks.

### [xml-validator](.agents/skills/xml-validator/SKILL.md)
* **Description:** Use this skill when XML files need to be edited, created, or validated against an XSD schema (or an existing DTD).
* **Location:** [.agents/skills/xml-validator/](.agents/skills/xml-validator/)
* **Usage:**
  * **Single File Validation:** Run the validation script specifying the XML file and the schema (`.xsd` or `.dtd`):
    ```powershell
    python .agents/skills/xml-validator/validate.py <file.xml> <schema.xsd/dtd>
    ```
  * **Bulk Validation:** To validate all block definitions ("Bausteine") in the workspace directories (data libraries, test workspaces) against an auto-generated Clean-Room XSD:
    ```powershell
    python .agents/skills/xml-validator/validate.py --bulk
    ```

### [iec61499-validator](.agents/skills/iec61499-validator/SKILL.md)
* **Description:** Use this skill to validate IEC 61499 XML files (e.g. `.fbt`, `.sub`) for reserved keywords and Structured Text (ST) syntax compliance.
* **Location:** [.agents/skills/iec61499-validator/](.agents/skills/iec61499-validator/)
* **Usage:**
  * **Single File Validation:** Run the validator on the XML file:
    ```powershell
    python .agents/skills/iec61499-validator/validator.py <file.xml>
    ```

---

## Available Subagents

Subagents can be invoked to perform tasks in separate contexts, helping organize work or delegate tasks.

* **research**: A read-only subagent for exploring the codebase and reading files. Best used when a task requires many search and read operations that would clutter the main context.
* **self**: A subagent inheriting the full configuration, tools, and system prompts of the parent agent, capable of executing write operations and running commands.
