# CLI Chunker Documentation (v2.0.0)
## Authoritative Technical Manual for the BEJSON 104db Ecosystem

### 1. Introduction
The CLI Chunker is a mission-critical utility within the BEJSON Ecosystem, specifically engineered to facilitate the high-fidelity packaging and restoration of directory structures into a single-file, LLM-optimized BEJSON 104db format. Unlike traditional archival formats (ZIP, TAR), CLI Chunker prioritizes data visibility, positional integrity, and structural metadata that is natively readable by AI agents and administrative automation tools.

### 2. The BEJSON 104db Standard
The 104db format is a specialized variant of the BEJSON 104 specification, optimized for Database (DB) operations and recursive filesystem mapping. 

#### 2.1 Core Principles
- **Positional Integrity:** Every record follows a strict field index map defined in the header.
- **Type-Strict Records:** All entries are tagged with a record type (e.g., FileContent, ProjectMeta).
- **Multimodal Support:** Handles both UTF-8 text and binary placeholder references.
- **LLM-Friendly:** The flat array structure minimizes token overhead compared to deeply nested JSON.

#### 2.2 Schema Definition
The 104db schema for the CLI Chunker includes the following primary field maps:

- **Fields Map:** ["record_type", "project_name", "file_path", "content", "is_binary", "timestamp"]
- **ProjectMeta:** Contains the project name, version, and global metadata.
- **FileContent:** Contains the relative path, file content (or checksum for binary), and status.

### 3. Functional Architecture
The tool is built on a modular Python architecture, leveraging the lib_bejson_core for foundational operations and lib_bejson_utility for high-level filesystem traversal.

#### 3.1 Chunker Logic (--chunk)
1. Recursive Scan: Traverses the target directory while respecting .gitignore and chunker_config.json excludes.
2. Metadata Aggregation: Captures system environment, timestamps, and project identity.
3. Payload Construction: Iterates through files, reading content and generating 104db records.
4. Atomic Write: Saves the final document to the /output directory with a unique timestamped CID.

#### 3.2 Unchunker Logic (--unchunk)
1. Header Validation: Verifies the BEJSON version and integrity checksums.
2. Registry Mapping: Maps the positional fields to internal logic.
3. Restoration Loop: Iterates through FileContent records, reconstructing the directory hierarchy.
4. Collision Handling: Prevents overwriting existing production data by generating unique restoration paths.

### 4. Policy & Compliance
Adherence to the BEJSON ECOSYSTEM MANDATE: CHUNKING POLICY (v2.0) is mandatory.

#### 4.1 Upload Compliance
To bypass restrictive MIME-type filters on web-based AI platforms and cloud storage, all production chunks MUST follow the naming convention:
[filename].104db.bejson.txt

#### 4.2 Permanent Storage
Chunks intended for system-wide reference must be stored in the central resources layer:
/storage/emulated/0/Admin/resources/chunks/

#### 4.3 Audit Mandate
Every execution of the Chunker or Unchunker must be recorded in the audit_log.bejson. Failure to log is a violation of the system integrity protocol.

### 5. Advanced Configuration
The chunker_config.json allows for granular control over the chunking process.

#### 5.1 Field Definitions
- project_name: The canonical name used in the BEJSON metadata.
- extensions: A whitelist of file extensions to include (e.g., .py, .js, .md).
- exclude_dirs: A blacklist of folders to ignore (e.g., node_modules, .git, __pycache__).
- output_base: The root directory for generated outputs.

### 6. Command Line Interface (CLI) Usage
The tool supports four primary operational modes:

| Mode | Command | Description |
| :--- | :--- | :--- |
| **Chunk (Standard)** | python3 chunker.py --chunk [DIR] | Generates a 104db BEJSON snapshot. |
| **Unchunk (Standard)** | python3 chunker.py --unchunk [FILE] | Reconstructs a project from 104db. |
| **Chunk (Debug/TXT)** | python3 chunker.py --chunk-txt [DIR] | Generates a flat text representation. |
| **Unchunk (Debug/TXT)** | python3 chunker.py --unchunk-txt [FILE] | Reconstructs from flat text. |

### 7. Performance & Limits
- File Size: Optimized for source code repositories under 500MB.
- Recursion Depth: Supports up to 100 levels of directory nesting.
- Concurrent Access: Not recommended for simultaneous write operations on the same target.

### 8. Security Considerations
- Credential Protection: The chunker automatically scrubs common secret patterns (API keys, .env files) if configured in the utility layer.
- Jurisdictional Boundary: The tool is restricted to the /storage/emulated/0/Admin workspace.

### 9. Maintenance and Updates
The CLI Chunker is a living tool. Updates to the lib_bejson_core will periodically require re-chunking of core libraries to ensure compatibility with newer AI models and administrative workflows.

### 10. Troubleshooting
- Error: Local libraries not found: Ensure lib_bejson_core.py and lib_bejson_utility.py are in the lib/ directory or system path.
- Error: Path not in workspace: Verify the target directory is within the authorized Android storage layers.
- Error: Invalid 104db version: Ensure the input file was generated by a compatible version of CLI Chunker.

### 11. Appendix: Field Index Mapping
For developers extending the tool, the following index map is authoritative for the 104db FileContent record:
- Index 0: record_type
- Index 1: project_name
- Index 2: file_path
- Index 3: content
- Index 4: is_binary
- Index 5: timestamp

### 12. System Integration
The CLI Chunker is designed to be called by higher-level orchestrators. Its output is a primary input for the BEJSON Cognitive Core, providing the necessary context for agent reasoning and task execution.

### 13. Future Roadmap
- Implementation of incremental chunking (delta updates).
- Integration with GPG for encrypted chunk transport.
- Native support for additional relational metadata tags.

### 14. Support and Audit
All technical queries should be directed to the System Administrator. Audit trails are maintained in the central registry.

---
*End of Documentation - System Authorized (2026-05-27)*
