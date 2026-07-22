# Automation_scripts

A collection of automation scripts designed to streamline system administation, file management and workflow tasks.

This repository serves as a centralized "toolbox" for utilities written primarily in Python, focusing on efficiency, clean code, and practical system automation.

## 📁 Repository Structure

* `scripts/` - Contains the executable source code for each automation tool.
* `docs/` - Comprehensive documentation, setup guides, and technical breakdowns for each script.

---

## 🛠️ Available Scripts

### 1. Automated File Organizer
* **Description:** Scans specified directories (e.g., Downloads) and dynamically categorizes files into structured subfolders based on extension types. 
* **Core Tech:** Python (`os`, `pathlib`, `sys`, `time`)
* **Links:** [Source Code](scripts/file_organizer.py) | [Detailed Documentation](docs/file_organizer.md)

### 2. pls
* **Description:** Lists entries in a given path with info about the size and permissions.
* **Core Tech:** Python (`os`, `pathlib`, `argparse`)
* **Links:** [Source Code](scripts/pls.py) | [Detailed Documentation](docs/pls.md)

*(More scripts will be added as they are developed.)*

---

## Getting started

### 1. Clone the repository
``` git clone https://github.com/Jardennn/Automation_scripts.git && cd Automation_scripts ```

### 2. Execution
Run any script from the scripts available on the scripts directory, replace [script_name] with your desired script.
``` python scripts/[script_name] ```
