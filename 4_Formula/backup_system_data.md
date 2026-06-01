# 💾 System Data Backup — Formula

How we secure, version, and backup the core exam and configuration data of the study mastery system.

---

## 🗺️ Backup Strategy

The core study data is located in `5_Symbols/data/`. This directory holds both local source data and generated JSON files consumed by the frontend and edge worker components.

```
5_Symbols/data/
    ├── exam.json          (Local questions repository)
    ├── exam_source.pdf    (Source material)
    ├── menu.json          (Navbar configuration)
    ├── pro-exam.json      (Advanced questions configuration)
    ├── questions.json     (Core exam database)
    └── search_index.json  (Search catalog)
```

To prevent data loss during manual editing, schema updates, or API interactions, a Python backup utility compresses all database state files and Azure Blob containers (if configured) into timestamped ZIP files stored in a dedicated `backups/` directory.

---

## ⚙️ How it Works

The backup script ([backup_data.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/backup_data.py)) automates:
1. Scanning `5_Symbols/data/` for data files (ignoring subdirectories like `backups/`).
2. Checking for the `AZURE_STORAGE_CONNECTION_STRING` environment variable.
3. If the environment variable is not set, dynamically querying Azure Key Vault `dp-kv-deliverypilot` for the secret `AzureWebJobsStorage` using `az keyvault secret show`.
4. Connecting to Azure Blob Storage to download files from key containers:
   - `memory-cards`
   - `analyse-pages`
   - `concepts`
4. Creating a transient sandbox directory containing all gathered files.
5. Compressing the targets using standard ZIP format.
6. Saving the timestamped archive under `5_Symbols/data/backups/backup_YYYYMMDD_HHMMSS.zip`.
7. Self-cleaning the transient directories.

---

## 🚀 Usage Guide

### Run Backup
Run the backup script directly using Python:
```bash
python3 5_Symbols/scripts/backup_data.py
```

### Restore Data from Backup
To restore data to a previous state:
1. Locate the desired ZIP archive in `5_Symbols/data/backups/`.
2. Extract the files from the archive.
3. Replace the active data files in `5_Symbols/data/` with the extracted files.

---

## 🧪 Verification Check

- [x] Run script to confirm it creates the `backups` folder.
- [x] Check that only target files are included in the generated ZIP file.
- [x] Verify zip extraction recovers intact JSON structure.
