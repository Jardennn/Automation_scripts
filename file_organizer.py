import pathlib
from pathlib import Path
import os
import getpass
import time

username = getpass.getuser()

# Checking if directories exist
parent = f"/home/{username}/tests"
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
        path.mkdir(parents=True, exist_ok = True)

while (True):
    all_entries = os.listdir(f"/home/{username}/tests")
    files = [f for f in all_entries if os.path.isfile(os.path.join(os.path.join(parent, f)))]
    print(f"Watching {parent} for files...")

    for file in files:
        file_alone = file
        file = f"/home/{username}/tests/{file}"
        file_ext = Path(file).suffix.lower()
        print(f"{file_alone} found! Moving to appropriate directory...")

        # Checks the file extension and moves to the appropriate
        match (file_ext):
            case (".txt"):
                os.rename(file, f"{parent}/txt/{file_alone}")
            case (".pdf"):
                os.rename(file, f"{parent}/pdf/{file_alone}")
            case (".zip"):
                os.rename(file, f"{parent}/zip/{file_alone}")
            case (".iso"):
                os.rename(file, f"{parent}/iso/{file_alone}")
            case (_):
                os.rename(file, f"{parent}/other_files/{file_alone}")

    # A minute wait time between file scans/moves, for giving the CPU some overhead time (My CPU burnt hot when I ran this on 2 seconds delay)
    time.sleep(60)
