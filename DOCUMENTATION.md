# CLI Chunker Documentation (v2.5.0)
## Authoritative Technical Manual for the BEJSON 104db Ecosystem

### 1. Introduction
The CLI Chunker is a mission-critical utility within the BEJSON Ecosystem, specifically engineered to facilitate the high-fidelity packaging and restoration of directory structures into a single-file, LLM-optimized BEJSON 104db format. Unlike traditional archival formats (ZIP, TAR), CLI Chunker prioritizes data visibility, positional integrity, and structural metadata that is natively readable by AI agents and administrative automation tools.

### 2. The BEJSON 104db Standard
The 104db format is a specialized variant of the BEJSON 104 specification, optimized for Database (DB) operations and recursive filesystem mapping. 

#### 2.1 Core Principles
- **Positional Integrity:** Every record follows a strict field index map defined in the header.
- **Type-Strict Records:** All entries are tagged with a record type (e.g., `FileContent`, `ProjectMeta`).
- **Multimodal Support:** Handles both UTF-8 text and binary placeholder references.
- **LLM-Friendly:** The flat array structure minimizes token overhead compared to deeply nested JSON.

#### 2.2 Schema Definition
The 104db schema for the CLI Chunker includes the following primary field maps:

- **ProjectMeta Fields:** `[Record_Type_Parent, project_name, version, root_path]`
- **FileContent Fields:** `[Record_Type_Parent, file_path, file_name, content, is_binary]`

### 3. Functional Architecture
The tool is built on a modular Python architecture, leveraging `lib_bejson_core` for foundational operations and `lib_bejson_utility` for high-level filesystem traversal.

#### 3.1 Chunker Logic (`--chunk`)
1. **Recursive Scan**: Traverses the target directory while respecting standard excludes (e.g., `.git`, `node_modules`).
2. **Project Registry**: Automates project tracking. If a directory has been chunked before, it updates its registration; otherwise, it creates a new entry.
3. **Versioned Storage**: Every chunk is stored in a dedicated version folder (`v1`, `v2`, etc.) within the `Projects/` hierarchy.
4. **Atomic Write**: Saves the final document with a `.txt` extension to ensure compatibility with web-based LLM interfaces.

#### 3.2 Unchunker Logic (`--unchunk`)
1. **Structural Validation**: Verifies the BEJSON 104db integrity before restoration.
2. **Registry Mapping**: Dynamically resolves field indices to ensure forward compatibility with schema updates.
3. **Restoration**: Reconstructs the directory hierarchy, restoring file contents accurately.
4. **Custom Destinations**: Supports the `--dest` flag to override the default restoration path.

### 4. Indexing & Management
CLI Chunker features a robust indexing system to manage growing project archives.

#### 4.1 Project Registry
Tracks the original source paths of projects.
- **List Index**: `python3 Cli_Chunker.py --list-project-index`
- **Re-chunk by ID**: `python3 Cli_Chunker.py --chunk-index 1`

#### 4.2 History Tracking
Records every chunking event for quick restoration.
- **List History**: `python3 Cli_Chunker.py --list-unchunk-index`
- **Restore by ID**: `python3 Cli_Chunker.py --unchunk-index 1`

#### 4.3 Cleanup Operations
- **Expell Project**: Removes a project from the registry but keeps its files (`--expell-project <ID>`).
- **Delete Project**: Removes project and permanently deletes all its chunk versions (`--delete-project <ID>`).
- **Delete Version**: Surgically removes a specific version folder (`--delete-version <ID> <VER>`).

### 5. Compliance & Security
- **MIME Evasion**: All chunks utilize the `.bejson.txt` dual-extension to bypass security filters on upload.
- **Atomic Operations**: Utilizes temporary file renaming to prevent data loss during power failures or crashes.
- **Path Portability**: Automatically handles relative and absolute paths across environments.

### 6. Command Map Summary

| Command | Category | Description |
| :--- | :--- | :--- |
| `--chunk DIR` | Chunker | Create a new versioned chunk from a directory. |
| `--chunk-index ID` | Chunker | Update an existing project snapshot by its ID. |
| `--unchunk FILE` | Unchunker | Restore a project from a specific BEJSON file. |
| `--unchunk-index ID`| Unchunker | Restore from a historical snapshot ID. |
| `--list-project-index`| Management | List all registered projects and their source paths. |
| `--list-unchunk-index`| Management | List historical snapshots with timestamps. |
| `--get-versions ID` | Management | List all saved version folders for a project. |
| `--delete-version ID V`| Management | Delete a specific version folder. |
| `--expell-project ID`| Management | Unregister a project (files preserved). |
| `--delete-project ID`| Management | Fully wipe a project and all its archives. |

### 7. Troubleshooting
- **Permission Denied**: Ensure `python3` is used to execute the script.
- **Missing lib/**: Ensure the tool's `lib/` directory contains `lib_bejson_core.py` and `lib_bejson_utility.py`.
- **Validation Error**: The input file may be corrupted or not a valid BEJSON 104db file.

---
*Manual Version: 2.5.0*
*System Authorized (2026-06-10)*
