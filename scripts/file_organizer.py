import os
import pathlib
import sys
import time
from pathlib import Path


def get_watch_directory():

    # Getting directory from user if provided
    if len(sys.argv) > 1:
        watch_path = Path(sys.argv[1]).expanduser().resolve()

    # Defaulting to the Downloads folder
    else:
        watch_path = Path.home() / "Downloads"
        print(f"[INFO] No path provided. Using default {watch_path}")

    # Error handeling
    if not watch_path.exists():
        print(f"[ERROR] The directory '{watch_path}' does not exist.")
        sys.exit(1)

    if not watch_path.is_dir():
        print(f"[ERROR] '{watch_path}' is a file, not a directory.")
        sys.exit(1)

    if not (os.access(watch_path, os.R_OK) and os.access(watch_path, os.W_OK)):
        print(
            f"[ERROR] Permission error, READ and WRITE permission required for '{watch_path}"
        )
        sys.exit(1)

    critical_paths = ["/", "/etc", "/var", "/bin", "/boot", "/usr"]
    if str(watch_path) in critical_paths:
        print(
            "[ERROR] System directory detected, sorting a system directory is dangerous."
        )
        sys.exit(1)

    return watch_path


# Collecting directories and entries as variables
parent = get_watch_directory()
entries = os.listdir(parent)
target = {"txt", "pdf", "zip", "iso", "other_files"}
existing = []

for name in entries:
    full = os.path.join(parent, name)
    # Finds the existing target directories
    if name in target:
        print(f"{name} directory found in {full}")
        existing.append(name)

# Removing the existing target directories from the list
missing_targets = set(target) - set(existing)

# Checking if there are missing targets and making them if there are
if missing_targets:
    print("Missing directories found, making them.")
    for missing in missing_targets:
        path = Path(f"{parent}/{missing}")
        print(f"Making {missing}")
        path.mkdir(parents=True, exist_ok=True)


print(f"Watching '{parent}' for files")
while True:
    # List only the files
    files = [f for f in parent.iterdir() if f.is_file()]

    for file in files:
        file_alone = file.name
        file_ext = file.suffix.lower()
        ext_only = file_ext.replace(".", "")
        print(f"{file_alone} found! Moving to appropriate directory...")

        # Checks the file extension and moves to the appropriate
        if ext_only in target and ext_only != "":
            dest_dir = Path(f"{parent}/{ext_only}")
        else:
            dest_dir = Path(f"{parent}/other_files")

        target_path = Path(f"{dest_dir}/{file_alone}")
        counter = 1
        # Checks if the found file already exists in the target directory
        while target_path.exists():
            new_name = f"{Path(file_alone).stem}({counter}){file_ext}"
            target_path = Path(f"{dest_dir}/{new_name}")
            counter += 1

        try:
            file.rename(target_path)
            print(f"[INFO] Successfully moved {file_alone} to {target_path}")

        # More error handling but with the actual file moving
        except PermissionError:
            print(
                f"[ERROR] Permission error moving file {file_alone}. File currently in use or missing permissions to move."
            )
            continue

        except FileNotFoundError:
            print(f"[ERROR] {file_alone} was not found in the source path.")
            continue

        except Exception as e:
            print(
                f"[ERROR] An unexpected error occurred while moving {file_alone}: {e}"
            )
            continue

    # A minute wait time between file scans/moves, for giving the CPU some overhead time (My CPU burnt hot when I ran this on 2 seconds delay)
    time.sleep(60)
