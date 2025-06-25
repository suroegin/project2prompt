# project2prompt

Collects all project files with the specified extensions and included paths into a single Markdown file.

## Usage
usage: project2prompt [-h] -l LANG -p PATH [-i [INCLUDE ...]] [-e [EXCLUDE ...]]

## Options

```
  -h, --help            show this help message and exit
  -l, --lang LANG       File extensions for searching, separated by commas (e.g., 'go,yaml,env').
  -p, --path PATH       Path to the root folder of the project.
  -i, --include [INCLUDE ...]
                        Paths to files or directories that need to be included, separated by spaces (e.g., 'folder1 file.txt').
  -e, --exclude [EXCLUDE ...]
                        Paths to files or directories that need to be excluded, separated by spaces (e.g., 'folder1 file.txt').
```
