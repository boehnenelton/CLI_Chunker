---
project_name: Cli_Chunker
version: 2.5.0
status: Agent-Ready
relational_id: gcli-tool-cli-chunker-001
---

# Cli Chunker: Agentic Project Packager (AX-2026)

[Agent-Ready] [MCP-Compatible] [llms.txt: Verified]

Cli Chunker is a high-density project snapshot utility designed for the 2026 AI-Native development lifecycle. It transforms entire directory structures into single, high-fidelity BEJSON 104db payloads for rapid delivery to Large Language Models (LLMs) or for transient versioning.

## 1. The Core Philosophy
In the 2026 ecosystem, 'context is currency.' Cli Chunker focuses on transient context snapshots. It is optimized for speed, numeric indexing, and 'zero-config' operation, making it the primary tool for feeding codebase state into reasoning agents.

## 2. Quick Start (One-Liner)
=> Execute(chunk_dir) -> Success
python3 Cli_Chunker.py --chunk ~/my-project

## 3. High-Density Command Map

| Command | Action | Mission |
| :--- | :--- | :--- |
| --list-project-index | Discovery | List registered projects with numeric IDs. |
| --chunk-index <ID> | Re-Chunk | Rapidly update a project by its registry ID. |
| --list-unchunk-index | Forensic | List historical chunks for restoration. |
| --unchunk-index <ID> | Restore | Rebuild a project from a historical ID. |
| --get-versions <ID> | Audit | View all saved version folders for a project. |
| --delete-version <ID> <v>| Prune | Surgically remove a specific version folder. |

## 4. Documentation Stack
- Execution Grounding: AGENTS.md
- Discovery Index: llms.txt
- Operational Logic: OPERATIONAL.md
- Typed Specification: SPECIFICATION.md

## 5. Security & Compliance
- Atomic Writes: Uses lib_bejson_core for corruption-proof persistence.
- MIME Evasion: Appends .txt to BEJSON chunks to bypass web upload filters.
- Relational Integrity: Maintains a project_registry.104a.bejson for source path tracking.

---
Author: Elton Boehnen
Contact: eltonboehnen@gmail.com
GitHub: github.com/boehnenelton
Version: 2.5.0