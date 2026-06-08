# File organizer

An automatically sort files to their extension folder (e.g. text.txt -> txt/text.txt)

---

## Overview

The purpose of the script is to sort files out to folders matching their extension.
This script solves the problem of loose unorganized files in folders (e.g. Downloads) and help find the specific file types you need. This saves time from looking inside the folder for the file by specifying it to the file type. 

### Key Features:

* **Feature 1:** Dynamic file sorting according to extension
* **Feature 2** Automated sub-directory initial existence check and missing directories generation 

---

## Technical Architecture and Workflow

### System Workflow

1. **Target evaluation and metadata collection:** The script initializes by collecting metadata like: the user logged in, the directory to watch, target directory entries, and sub-directories names.

2. **Initial sub-directories check:** Firstly, when the script runs; it checks for the existing sub-directories in the parent folder and makes the missing sub-directories from the sub-directories list.

3. **Looped file scan:** Scans every minute for files that exist in the root of the parent directory.

4. **File sorting:** If a file exist in the parent directory, the script gets the file extension and matches the folder to move the file to according to the extension given from the snipping.

### Core libraries / modules

* `os` / `pathlib` - Used for filesystem navigation, path management, and safely moving files and directories.

* `time` - Used to manage execution intervals and reduce CPU overhead.

---

## Prerequisites & Installation

### Dependencies

This script relies on Python standard libraries. There is no need for external packages installations.

### Environment Configurations

Before execution, verify that your local environment meets the following criteria:

* **Python version:** Python 3.10 or higher is recommended, due the match/case structures.

* **Permissions:** Read/Write access permissions granted for the existing sub-directories and parent directory.

---

## Usage and configuration

### Script customization (optional)

In order for customizing the script (e.g. changing parent directory/adding sub-directories to the list):

Open ` scripts/file_organizer ` in a text editor and adjust the configuration variables on top of the file.

* **Parent directory:** Change the `parent` path variable to your desired directory.

* **Sub-directories list:** Modify the `target_dirs` set. You can add or remove extensions seamlessly by updating the strings inside the braces:
```python target_dirs = {"txt", "pdf", "zip", "iso", "png", "other_files"} ```
Then you would need to add a case block in the while loop for moving files onto your modified directory.


