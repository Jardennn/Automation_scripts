import os
import sys
from pathlib import Path
import argparse
import stat
from datetime import datetime

parser = argparse.ArgumentParser(description="A script for displaying path entries", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--path", type=Path, help="The path of your directory to watch (relative or absolute), leave empty for using the current working directory")
parser.add_argument("-s", "--sort", choices=["size-desc", "size-asc", "A-Z", "Z-A"], type=str, help="""Sort the output. options:
size-desc - Sort the files from the biggest to smallest
size-asc - Sort the files from the smallest to biggest
A-Z - Sort the files alphetically
Z-A - Sort the files alphetically reversed""")
parser.add_argument("-a", "--all", action='store_true', help="Output all of the files in the given path")

args = parser.parse_args()

def get_directory():

    if args.path is not None:
        # Get the path from a user argument if provided
        dir = Path(args.path).expanduser().resolve()

    else:
        # If no argument provided, use the current working directory
        dir = Path.cwd().resolve()

    # == Error handeling ==

    # Check for existance
    if not dir.exists():
        print(f"[ERROR] The directory '{dir}' does not exist.")
        sys.exit(1)

    # Check if argument is file or directory (If is file will just display the path (Might change later))
    if not dir.is_dir():
        print(f"{dir}")
        sys.exit(1)

    # Check for READ permissions
    if not (os.access(dir, os.R_OK)):
        print(f"[ERROR] Permission error, READ permission missing for '{dir}'")
        sys.exit(1)

    return dir

dir = get_directory()
# Lists all entries in the given directory
entries = [item for item in dir.iterdir()]

def perms_to_string(perms):
    # item.stat().st_mode = int

    # Determine the file type character (Shifting 12 bits to find the type)
    file_type_code = (perms >> 12) & 15

    if file_type_code == 4: # If the found file type is octal 04, it will be determined as a directory
        file_type = "d"
    elif file_type_code == 8: # If the found file type is octal 08, it will be determined as a file
        file_type = "-"
    elif file_type_code == 12: # If the found file type is octal 12, it will be determined as a symlink
        file_type = "l"
    else: # If the found file type is anything else, it will be determined as unknown
        file_type = "?"

    # All possibilities for file permissions in readable format
    chars = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]

    # == Getting the permission bits ==
    owner = chars[(perms >> 6) & 7] # Shifting 6 bits to find the owner and striping 3 bits off the end
    group = chars[(perms >> 3) & 7] # Shifting 3 bits to find the group and striping 3 bits off the end
    others = chars[perms & 7] # Striping 3 bits off the end to find other permissions

    result = f"{file_type}{owner}{group}{others}" # Connecting all found stuff together
    return result

def sizes_convert(bytes):
    # Default size is in bytes

    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'] # List of sizes labels for conversion
    unit_index = 0

    while (bytes >= 1000) and unit_index < len(sizes) - 1: # Running while the bytes count is still above 999 and unit index doesn't go over the list
        bytes /= 1000 # Dividing 1000 out of the bytes, to calculate the file size label (e.g. 1000 Bytes = 1 Kilobytes)
        unit_index += 1

    return f"{bytes} {sizes[unit_index]}"

def remove_hidden(entries):
    filtered = []
    for item in entries:
        ishidden = item.name.startswith(".") # Checking if item is hidden in Linux and Mac system

        if os.name == "nt" and not ishidden: # For if the OS is Windows
            try:
                attrs = item.stat().st_file_attributes # Checking file attributes for hidden mark
                ishidden = bool(attrs & stat.FILE_ATTRIBUTE_HIDDEN) # Checking if item is hidden with the attribute in Windows systems

            except (AttributeError, OSError):
                pass

        if not ishidden: # If the file is not hidden it will be added to the filtered list
            filtered.append(item)

    return filtered

def sorts():
    # Sorting alphetically
    if args.sort == 'A-Z':
        new_entries = sorted(entries, key=lambda p: p.name.lower())
        
        return new_entries

    # Sorting alphetically in reverse
    if args.sort == 'Z-A':
        new_entries = sorted(entries, key=lambda p: p.name.lower())

        new_entries.reverse()
        
        return new_entries

    # Sorting by size ascending
    if args.sort == 'size-asc':
        new_entries = sorted(entries, key=lambda p: p.stat().st_size)

        return new_entries

    # Sorting by size decending
    if args.sort == 'size-desc':
        new_entries = sorted(entries, key=lambda p: p.stat().st_size, reverse=True)

        return new_entries

    return None

print("Permissions | Size | Date | Name")

if args.all is False:
    if sorts() != None:
        entries = sorts()

    filtered = remove_hidden(entries)
    for item in filtered:
        try:
            print(f"[{perms_to_string(item.stat().st_mode)}] | [{sizes_convert(item.stat().st_size)}] | [{datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")}] | [{item.name}]")
        except FileNotFoundError:
            continue

else:
    if sorts() != None:
        entries = sorts()

    for item in entries:
        try:
            print(f"[{perms_to_string(item.stat().st_mode)}] | [{sizes_convert(item.stat().st_size)}] | [{datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")}] | [{item.name}]")
        except FileNotFoundError:
            continue
