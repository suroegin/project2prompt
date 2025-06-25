import argparse
from pathlib import Path
import sys

def create_prompt_file(languages: list, project_path: str, include_paths: list, exclude_paths: list):
    root_path = Path(project_path)

    if not root_path.is_dir():
        print(f"Error: Path '{project_path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    include_paths = [root_path.joinpath(path) for path in include_paths]
    exclude_paths = [root_path.joinpath(path) for path in exclude_paths]

    files_to_process = set()
    for lang in languages:
        file_pattern = f"*.{lang}"
        files_to_process.update(root_path.rglob(file_pattern))

    for include_path in include_paths:
        if include_path.is_file():
            files_to_process.add(include_path)
        elif include_path.is_dir():
            files_to_process.update(include_path.rglob("*"))

    files_to_process = [
        file for file in files_to_process
        if not any(exclude_path in file.parents or exclude_path == file for exclude_path in exclude_paths)
    ]

    if not files_to_process:
        print(f"No files found with the specified extensions or included paths in '{project_path}'.")
        return

    project_name = root_path.name
    output_filename = f"{project_name}_prompt.md"

    print(f"Found {len(files_to_process)} files. Creating file {output_filename}...")

    try:
        with open(output_filename, "w", encoding="utf-8") as md_file:
            for file_path in files_to_process:
                relative_path = file_path.relative_to(root_path)
                # Определение языка для синтаксиса в Markdown
                language = file_path.suffix.lstrip('.')
                md_file.write(f"`{relative_path}`:\n\n")
                md_file.write(f"```{language}\n")

                try:
                    content = file_path.read_text(encoding="utf-8")
                    md_file.write(content)
                except UnicodeDecodeError:
                    md_file.write(f"Failed to read file {relative_path} (encoding error).")
                
                md_file.write("\n```\n\n")

        print(f"Successfully! File '{output_filename}' created in the current directory.")

    except IOError as e:
        print(f"Ошибка при записи файла: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Collects all project files with the specified extensions and included paths into a single Markdown file."
    )
    parser.add_argument(
        "-l", "--lang",
        type=str,
        required=True,
        help="File extensions for searching, separated by commas (e.g., 'go,yaml,env')."
    )
    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Path to the root folder of the project."
    )
    parser.add_argument(
        "-i", "--include",
        type=str,
        nargs='*',
        default=[],
        help="Paths to files or directories that need to be included, separated by spaces (e.g., 'folder1 file.txt')."
    )
    parser.add_argument(
        "-e", "--exclude",
        type=str,
        nargs='*',
        default=[],
        help="Paths to files or directories that need to be excluded, separated by spaces (e.g., 'folder1 file.txt')."
    )

    args = parser.parse_args()

    languages = args.lang.split(',')

    create_prompt_file(
        languages=languages,
        project_path=args.path,
        include_paths=args.include,
        exclude_paths=args.exclude
    )


if __name__ == "__main__":
    main()