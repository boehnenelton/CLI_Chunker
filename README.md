# CLI Chunker (v2.0)
## High-Fidelity BEJSON 104db Project Snapshoting

CLI Chunker is the standard tool for packaging software projects into AI-friendly BEJSON 104db files. It ensures structural integrity, metadata retention, and rapid ingestion for large language models and automated agents.

### 🚀 Quick Start
```bash
# Chunk a project
python3 chunker.py --chunk /path/to/project

# Unchunk a BEJSON file
python3 chunker.py --unchunk /path/to/snapshot.104db.bejson
```

### 📜 Core Mandates
1. **Format:** Always use --chunk (104db) for production-grade snapshots.
2. **Naming:** Append .txt to your .bejson files for web compliance (e.g., data.104db.bejson.txt).
3. **Storage:** Move final chunks to /storage/emulated/0/Admin/resources/chunks/.
4. **Audit:** Every chunking action MUST be recorded in the system audit_log.bejson.

### 📂 Repository Structure
- chunker.py: The main CLI entry point.
- lib/: Core BEJSON and Utility libraries (symbolic links recommended).
- output/: Default location for generated chunks and restorations.
- DOCUMENTATION.md: Comprehensive technical manual and policy guide.

### 📊 BEJSON 104db Schema Example
The following is an example of the internal structure of a generated chunk:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104db",
  "Fields": [
    {"name": "record_type", "type": "string"},
    {"name": "project_name", "type": "string"},
    {"name": "file_path", "type": "string"},
    {"name": "content", "type": "string"},
    {"name": "is_binary", "type": "boolean"},
    {"name": "timestamp", "type": "string"}
  ],
  "Values": [
    ["ProjectMeta", "MyTool", null, "Version 2.0.0", false, "20260527T1200Z"],
    ["FileContent", "MyTool", "main.py", "print('hello')", false, "20260527T1205Z"],
    ["FileContent", "MyTool", "config.json", "{\"debug\": true}", false, "20260527T1206Z"]
  ]
}
```

### 🛠️ Advanced Operations
- Use --chunk-txt for a human-readable flat text dump of the project structure.
- Use --unchunk-txt to rebuild a project from a previously generated flat text dump.
- Check chunker_config.json in your target directory to customize exclusion rules.

### 🛡️ Security
This tool is designed for use in the BEJSON Ecosystem. It respects workspace boundaries and provides automated metadata tagging for audit compliance.

### 📝 Development Status
- Stable Version: 2.0.0
- Next Release: 2.1.0 (Incremental Chunking)

---
*Created by Elton Boehnen - 2026*
