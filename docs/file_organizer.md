# File organizer

An automatically sort files to their extension folder (e.g. text.txt -> txt/text.txt)

---

## Overview

The purpose of the script is to sort files out to folders matching their extension.
This script solves the problem of loose unorganized files in folders (e.g. Downloads) and help find the specific file types you need. This saves time from looking inside the folder for the file by specifying it to the file type. 

### Key Features:

* **Feature 1:** Dynamic file sorting according to extension

* **Feature 2** Automated sub-directory initial existence check and missing directories generation 

* **Feature 3:** Option to select custom watch path from system arguments, with error handling to detect problems with the given path.

* **Feature 4:** Duplication avoidance, the script prevents duplication of files in the target folder by checking if the file exists on the target path and changing the number of file name it is on the directory.

* **Feature 5:** Error handling to output an error about: Permissions error, file absence and other unspecified errors.

---

## Technical Architecture and Workflow

### System Workflow

1. **Watch path collection:** The script collects the path given by the user when executing by adding the desired path as an argument. If no argument was given, the script will default to the Downloads folder of the system. There is also error handeling for if the given argument is problematic, the script will notify the user about it and exit the script.

2. **Target evaluation and metadata collection:** The script initializes by collecting metadata like: the directory to watch, target directory entries, and sub-directories names.

3. **Target directory existence check:** Checks for existence of the target directory. If the directory doesn't exist, the script will make it and if it does exist it will skip this step. This is used for the instance if the default Downloads directory or if the given directory argument doesn't exist. 

4. **Sub-directories check:** After the metadata collection and initial checks, the script checks for the existing sub-directories in the parent folder and makes the missing sub-directories from the sub-directories list.

5. **Looped file scan:** Scans every minute for files that exist in the root of the parent directory.

6. **File sorting:** Gets the file extension and matches it to the corresponding sub-directory. If no folder exists for that extension, the file is moved to the `other_files` sub-directory.

7. **Duplicate handling:** If a file of the same name exists already on the target sub-directory, a number will be appended to the filename to avoid overwriting.

8. **Error handling:** Catches permissions errors, missing file errors (file doesn't exists in the source path), and general unexpected errors in the sorting of the file.

### Core libraries / modules

* `os` / `pathlib` - Used for filesystem navigation, path management, and safely moving files and directories.

* `time` - Used to manage execution intervals and reduce CPU overhead.

* `sys` - Used for getting arguments on execution. 

---

## Prerequisites & Installation

### Dependencies

This script relies on Python standard libraries. There is no need for external packages installations.

### Environment Configurations

Before execution, verify that your local environment meets the following criteria:

* **Python version:** Python 3.10 or higher is recommended,

* **Permissions:** Read/Write access permissions granted for the existing sub-directories and parent directory.

---

## Usage and configuration

### Script customization (optional)

In order for customizing the script (e.g. changing parent directory/adding sub-directories to the list):

* **Parent directory:** 
Add a system argument in the execution command of the script. Example:
```
python file_organizer.py /path/to/watch
```
The code above assumes you're executing the script from the same directory as the script is in. Replace `/path/to/watch` with your desired path.


* **Sub-directories list:** Open `scripts/file_organizer` in a text editor and adjust the configuration variables right under the custom path collection.

Modify the `target_dirs` set. You can add or remove extensions seamlessly by updating the strings inside the braces:
```python 
target = {"txt", "pdf", "zip", "iso", "png", "other_files"} 
```


