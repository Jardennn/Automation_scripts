# pls

Script for listing files with their permissions and size beside them 

---

## Overview

This script's purpose is to display files in a detailed and organized way, I was in need for a solution to display file sizes in bigger labels (GBs, TBs) instead of just bytes.

### Features:

* **System arguments:** You can pass system arguments to the script. The existing flags:
  * **`-p`/`--path`:** Allows you to pass a path to list, relative or absolute. If not placed the script will use the current working directory. Requires an argument.
  * **`-a`/`--all`:** List all files in the given path.
  * -s/--sort: Sorting options for the output. 
    * 'A-Z': Sorting the output alphabetically
    * 'Z-A': Sorting the output alphabetically reversed
    * 'size-asc': Sorting the output by ascending size
    * 'size-desc': Sorting the output by descending size

* **Readable permissions:** The permissions and file type are calculated from their octal code to labels.

* **Size label conversion:** File sizes are displayed in the largest human readable unit. (e.g. File.txt = 1KB). 1000 Bytes => 1KB 

* **Cross platform:** The script itself is cross platform, but there is also a function to detect a Windows file system for detecting hidden files.

* **Error handling:** There are error handling to show errors about non existing paths and permissions errors.

---

## Technical Architecture and Workflow

### Workflow

This workflow will focus on if no flags are passed but it will explain the if statements.

1. **Path and entries collection:** The script gets the target directory by checking if the argument was passed, if not it defaults to the current working directory. Then there are checks for if the path exists and if it's readable, if the path is a file the script will print the path (will be changed). After collecting the path it will get the entries for the path.

2. **Check for '-a' flag passage and removing hidden paths:** The script will check if the 'all' flag was passed. if it was the script will display the full list of entries for the given path. if not, it will remove the hidden paths and continue with a filtered list.

3. **Sorting detection:** The script will run the sorting function and detect if the function did not return 'None'. if it didn't return 'None' it will replace the existing entries with the returned entries by the function.

4. **Removing hidden paths:** The `remove_hidden` function recieves the entries list and generates a new filtered list. It will go through every item in the entries and ask if they're hidden, first on Linux and Mac (using the .file), and then on Windows (File attributes). If the file was not found to be hidden (`ishidden = False`) it will be added to the filtered list.

5. **Converting permissions from octal to readable:** The script now goes over every item in the entries/filtered list and passed the item onto the `perm_to_string` function. This function first calculates the file type (Directory, file, symlink) by calculating with octals and binary out of the given octal data from running `item.stat().st_mode`. After that it will calculate the permissions for owner, group, and others against all readable combinations. The owner being at the start (shifted 6 bits and striped the 3 last bits), the group in the middle (shifted 3 bits and striped the 3 last bits) and the others being at the end with just the last 3 bits striped. Then the result will be returned as `<file_type><owner><group><others>`

6. **Size label conversion:** The `sizes_convert` function recieves the bytes count as an argument, and it has a list of labels and a variable for the index. Then it calculates the label by running a loop as long as the bytes are above and equal to 1000 Bytes that divides the bytes by a 1000 and adds to the index +1 value. This is called a unit scaling loop, it divides the current value by powers of 1000 It shifts the number up to the next storage metric. Formula: `Current_value = Starting_bytes/1000^loop_count`

7. **Prints out the output:** The scripts now finally prints out the output containing the calculated file size and label and permissions with the file name at the end in this format. `Permissions | Size | Name`   

### Core libraries / modules

* `os` / `pathlib` - Used for the filesystem navigation and displaying stats.

* `stat` - Used for extended file stats, mainly for Windows file attributes.

* `argparse` - For system arguments and flags.  

* datetime - Used for displaying the date and time of an entry in the output.

---

## Prerequisites & Installation

### Dependencies

This script relies on Python standard libraries. There is no need for external packages installations.

### Environment Configurations

Before execution, verify that your local environment meets the following criteria:

* **Python version:** Python 3.8 or higher is recommended.

* **Permissions:** Read/access permissions granted for the target directory.

---

## Usage

```bash
python pls.py -p <path> --sort '<choice>' -a
```

The flags are not required for running the script but do extend the functionality of the script.

## Todo and future features

* Potentially add more data in the output and extend the functionality of the script.

