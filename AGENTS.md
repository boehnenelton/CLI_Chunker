# AGENTS.md: Operational Manual for Cli Chunker

## Strict Constraints
- Never modify files within the Projects/ directory manually. Use the CLI flags.
- Always use --chunk-index for registered projects to preserve version continuity.
- Do not bypass structural validation. If a chunk fails validation, abort the operation.

## Entry Points
- Master script: Cli_Chunker.py
- Local libs: lib/*.py (Core BEJSON logic)

## Commands for Agents
- Test Command: python3 Cli_Chunker.py --chunk ./test_dir
- Verification Command: python3 Cli_Chunker.py --list-project-index

## Context Routing
- Project storage: Projects/<ProjectName>/v<N>/
- Project Registry: project_registry.104a.bejson
- History Log: chunk_history.104a.bejson

## Reasoning Model
Cli Chunker uses a Versioned Folder Hierarchy. It does not use a central database for file contents; each version is a standalone BEJSON 104db file. This ensures that even if the registry is corrupted, the versioned files remain valid context snapshots.