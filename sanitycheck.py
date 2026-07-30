from pathlib import Path

paths = [
        Path("/home/jarden/c.txt"),
        Path("/home/jarden/a.txt"),
        Path("/home/jarden/b.txt") 
        ]

sortied = sorted(paths, key=lambda p: p.name)

sortied.reverse()

print(sortied)
