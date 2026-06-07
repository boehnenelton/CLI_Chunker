#===============================================================================
# BEJSON ECOSYSTEM MANDATE: CHUNKING POLICY (v2.0)
#===============================================================================
# [USAGE NOTE]: Use Cli_Chunker for TRANSIENT payloads, single-file context
# snapshots (BEJSON 104db), and rapid delivery to LLMs.
# NOT for long-term version history or lossless binary archiving.
# ALWAYS check and obey the Chunking Policy in the Policy Registry.
#
# 1. PERMANENT STORAGE: All final chunks MUST be stored in:
#    /storage/emulated/0/Admin/resources/chunks/
# 2. FORMAT STANDARD: ALWAYS use BEJSON 104db format for all production chunks.
# 3. UPLOAD COMPLIANCE: All .bejson chunks MUST append .txt to the filename.
#    This bypasses restrictive MIME-type filters on web platforms.
#    Example: library.104db.bejson.txt
# 4. CLEANUP: Delete temporary timestamped folders in /output/ after moving.
# 5. AUDIT: All chunking operations MUST be logged to the system Audit Log.
#===============================================================================

#!/usr/bin/env python3
"""
CLI Chunker - Project to BEJSON 104db Packager & Rebuilder
REMEDIATED: Strictly non-regex, uses lib_bejson_utility for parity.
"""
import os
import sys
import json
import argparse
import time
from pathlib import Path

# Setup local library path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "lib"))

try:
    import lib_bejson_core as BEJSONCore
    import lib_bejson_utility as Utility
    import lib_bejson_validator as Validator
except ImportError:
    print("CRITICAL: Local libraries not found in lib/")
    sys.exit(1)

HISTORY_FILE = BASE_DIR / "chunk_history.104a.bejson"
HISTORY_FIELDS = [
    {"name": "timestamp", "type": "string"},
    {"name": "project_name", "type": "string"},
    {"name": "file_path", "type": "string"}
]

DEFAULT_CONFIG = {
    "project_name": "MyProject",
    "version": "v1.6.0",
    "extensions": Utility.DEFAULT_EXTENSIONS,
    "exclude_dirs": Utility.DEFAULT_EXCLUDES,
    "output_base": str(BASE_DIR / "output"),
    "evade_mime": True
}

def get_timestamp():
    return Utility.bejson_utility_get_timestamp()

def load_or_create_config(target_path):
    config_path = Path(target_path) / "chunker_config.json"
    # Derive project name from directory name
    auto_name = target_path.name.replace(" ", "_")
    
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                # Auto-set name if default or missing
                if config.get("project_name") == "MyProject" or "project_name" not in config:
                    config["project_name"] = auto_name
                
                for k, v in DEFAULT_CONFIG.items():
                    if k not in config: config[k] = v
                return config
        except Exception as e:
            print(f"Warning: Failed to read config, using defaults. Error: {e}")
    
    # Create new config with derived name
    config = DEFAULT_CONFIG.copy()
    config["project_name"] = auto_name
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"[*] Created default config at {config_path}")
    except Exception as e:
        print(f"Warning: Could not create config file. Error: {e}")
        
    return config

def save_to_history(project_name, file_path):
    history = []
    if HISTORY_FILE.exists():
        try:
            doc = BEJSONCore.bejson_core_load_file(str(HISTORY_FILE))
            history = doc.get("Values", [])
        except: pass
    
    # Newest at top
    history.insert(0, [get_timestamp(), project_name, str(file_path)])
    history = history[:20] # Keep last 20
    
    doc = BEJSONCore.bejson_core_create_104a("ChunkHistory", HISTORY_FIELDS, history)
    BEJSONCore.bejson_core_atomic_write(str(HISTORY_FILE), doc)

def list_history():
    if not HISTORY_FILE.exists():
        print("No chunk history found.")
        return
    
    try:
        doc = BEJSONCore.bejson_core_load_file(str(HISTORY_FILE))
        values = doc.get("Values", [])
        if not values:
            print("History is empty.")
            return
            
        print(f"\n{'ID':<4} | {'Timestamp':<20} | {'Project':<20} | {'Path'}")
        print("-" * 80)
        for i, row in enumerate(values, 1):
            ts, proj, path = row
            print(f"{i:<4} | {ts:<20} | {proj:<20} | {path}")
    except Exception as e:
        print(f"Error reading history: {e}")

def resolve_history_index(index_str):
    if not HISTORY_FILE.exists(): return None
    try:
        idx = int(index_str) - 1
        doc = BEJSONCore.bejson_core_load_file(str(HISTORY_FILE))
        values = doc.get("Values", [])
        if 0 <= idx < len(values):
            return values[idx][2] # Index 2 is file_path
    except: pass
    return None

def run_chunk(target_dir):
    target_path = Path(target_dir).resolve()
    if not target_path.is_dir():
        print(f"Error: {target_dir} is not a directory.")
        return

    config = load_or_create_config(target_path)
    
    print(f"[*] Mode: CHUNK (104db)")
    print(f"[*] Target: {target_path}")
    
    doc = Utility.bejson_utility_create_cli_chunk(
        target_dir=target_dir,
        project_name=config["project_name"],
        version=config["version"]
    )
    
    # Structural Validation
    print("[*] Validating BEJSON structure...")
    res = Validator.validate_bejson(doc)
    if not res.valid:
        print("\n[ERROR] BEJSON Validation Failed:")
        for err in res.errors:
            print(f"  - {err}")
        return

    ts_slug = get_timestamp().replace(":", "").replace("-", "")
    out_dir = Path(config["output_base"]) / "chunked" / ts_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    
    ext = ".104db.bejson"
    if config.get("evade_mime"):
        ext += ".txt"
        
    out_file = out_dir / f'Chunked_{Utility.bejson_utility_sanitize_name(config["project_name"])}{ext}'
    
    if Utility.bejson_utility_save_chunk(str(out_file), doc):
        print(f"\n[SUCCESS] Project chunked into {out_file}")
        print(f"[*] Total Records: {len(doc['Values'])}")
        save_to_history(config["project_name"], out_file)
    else:
        print(f"\n[ERROR] Failed to save BEJSON chunk.")

def run_unchunk(arg):
    # Try to resolve index
    resolved_path = resolve_history_index(arg)
    bejson_file = resolved_path if resolved_path else arg
    
    input_path = Path(bejson_file).resolve()
    if not input_path.exists():
        print(f"Error: File {bejson_file} not found.")
        return

    print(f"[*] Mode: UNCHUNK")
    print(f"[*] Source: {input_path}")
    
    try:
        # Structural Validation
        print("[*] Validating BEJSON structure...")
        res = Validator.validate_bejson(str(input_path), is_file=True)
        if not res.valid:
            print("\n[ERROR] BEJSON Validation Failed:")
            for err in res.errors:
                print(f"  - {err}")
            return

        doc = BEJSONCore.bejson_core_load_file(str(input_path))
        if doc.get("Format_Version") != "104db":
            print("Error: Input is not a valid BEJSON 104db file.")
            return

        # Mapping indices based on field schema
        fields = [f["name"] for f in doc["Fields"]]
        pname_idx = fields.index("project_name")
        fpath_idx = fields.index("file_path")
        cont_idx = fields.index("content")
        bin_idx = fields.index("is_binary")
        
        # Manually filter records by type (104db discriminator is index 0)
        meta_rows = [r for r in doc["Values"] if r[0] == "ProjectMeta"]
        proj_name = meta_rows[0][pname_idx] if meta_rows else "RestoredProject"
        
        ts_slug = get_timestamp().replace(":", "").replace("-", "")
        # Setup Output Dir
        out_dir = Path(DEFAULT_CONFIG["output_base"]) / "unchunked" / ts_slug / Utility.bejson_utility_sanitize_name(proj_name)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract Files
        file_rows = [r for r in doc["Values"] if r[0] == "FileContent"]
        for row in file_rows:
            rel_path = row[fpath_idx]
            content = row[cont_idx]
            binary = row[bin_idx]
            
            if rel_path:
                target_file = out_dir / rel_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                if binary:
                    target_file.touch()
                else:
                    target_file.write_text(content, encoding="utf-8")
                print(f"  [>] {rel_path}")

        print(f"\n[SUCCESS] Project rebuilt at {out_dir}")

    except Exception as e:
        print(f"\n[ERROR] Unchunking failed: {e}")

def run_chunk_txt(target_dir):
    print("RESTRICTED: Flat text chunking is allowed for debugging only.")
    target_path = Path(target_dir).resolve()
    config = load_or_create_config(target_path)
    
    print(f"[*] Mode: CHUNK (TXT)")
    txt_content = Utility.bejson_utility_chunk_to_text(target_dir)
    
    ts_slug = get_timestamp().replace(":", "").replace("-", "")
    out_dir = Path(config["output_base"]) / "chunked" / ts_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{Utility.bejson_utility_sanitize_name(config['project_name'])}.txt"
    
    out_file.write_text(txt_content, encoding="utf-8")
    print(f"\n[SUCCESS] Project chunked into {out_file}")
    save_to_history(config["project_name"], out_file)

def run_unchunk_txt(txt_file):
    # Resolve index
    resolved_path = resolve_history_index(txt_file)
    input_file = resolved_path if resolved_path else txt_file
    
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: File {input_file} not found.")
        return
        
    print(f"[*] Mode: UNCHUNK (TXT)")
    
    content = input_path.read_text(encoding="utf-8")
    ts_slug = get_timestamp().replace(":", "").replace("-", "")
    out_dir = Path(DEFAULT_CONFIG["output_base"]) / "unchunked" / ts_slug / input_path.stem
    
    count = Utility.bejson_utility_unchunk_from_text(content, str(out_dir))
    print(f"\n[SUCCESS] Project rebuilt at {out_dir}")
    print(f"[*] Total Files: {count}")

def main():
    parser = argparse.ArgumentParser(description="BEJSON Project Chunker/Unchunker")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chunk", metavar="DIR", help="Chunk a directory into BEJSON")
    group.add_argument("--unchunk", metavar="FILE/ID", help="Unchunk a BEJSON file or history ID")
    group.add_argument("--chunk-txt", metavar="DIR", help="Chunk a directory into a text file")
    group.add_argument("--unchunk-txt", metavar="FILE/ID", help="Unchunk a text file or history ID")
    group.add_argument("--history", action="store_true", help="List recent chunking history")
    
    args = parser.parse_args()
    
    if args.history:
        list_history()
    elif args.chunk:
        run_chunk(args.chunk)
    elif args.unchunk:
        run_unchunk(args.unchunk)
    elif args.chunk_txt:
        run_chunk_txt(args.chunk_txt)
    elif args.unchunk_txt:
        run_unchunk_txt(args.unchunk_txt)

if __name__ == "__main__":
    main()
