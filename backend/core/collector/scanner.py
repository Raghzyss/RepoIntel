from pathlib import Path


IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "dist",
    "build",
    ".next",
    ".idea",
    ".vscode",
}


SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".mts",
    ".cts",
    ".java",
    ".cpp",
    ".cc",
    ".c",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".kts",
    ".html",
    ".css",
    ".scss",
    ".sass",
    ".sql",
    ".sh",
}


CONFIG_FILES = {
    # JavaScript / Node
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",

    # Python
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",

    # Java
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",

    # Go / Rust
    "go.mod",
    "Cargo.toml",

    # Docker
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",

    # Configuration
    ".gitignore",
    ".editorconfig",
    "tsconfig.json",

    # Frontend configs
    "next.config.js",
    "next.config.ts",
    "next.config.mjs",
    "vite.config.js",
    "vite.config.ts",
    "vite.config.mjs",
    "tailwind.config.js",
    "tailwind.config.ts",
    "tailwind.config.mjs",

    # Documentation
    "LICENSE",
    "LICENSE.md",
    "LICENCE",
    "LICENCE.md",
    "CHANGELOG",
    "CHANGELOG.md",
    "HISTORY.md",
    "CONTRIBUTING",
    "CONTRIBUTING.md",
    "SECURITY",
    "SECURITY.md",
    "CODE_OF_CONDUCT",
    "CODE_OF_CONDUCT.md",
    "CITATION.cff",
}


class RepositoryScanner:

    def scan(self, repository):

        root_readme = None

        for path in repository.local_path.rglob("*"):

            if any(part in IGNORE_DIRS for part in path.parts):
                continue

            relative_path = path.relative_to(repository.local_path)
            repository.folder_tree.append(str(relative_path))

            if path.is_dir():
                repository.directories.append(path)
                continue

            repository.total_files += 1

            # File size
            try:
                repository.file_sizes[path] = path.stat().st_size
            except Exception:
                repository.file_sizes[path] = 0

            # File content
            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                repository.file_contents[path] = content
                repository.total_lines += len(content.splitlines())

            except Exception:
                repository.file_contents[path] = ""

            # Source files
            if path.suffix.lower() in SOURCE_EXTENSIONS:

                repository.source_files.append(path)

                repository.files_by_extension.setdefault(
                    path.suffix.lower(),
                    []
                ).append(path)

            filename = path.name.lower()

            # Config files
            if filename in CONFIG_FILES:
                repository.config_files[filename] = path

            # README detection
            if filename.startswith("readme"):

                if path.parent == repository.local_path:
                    root_readme = path

                elif root_readme is None:
                    root_readme = path

        # Read README once
        if root_readme:

            repository.readme_path = root_readme

            try:
                repository.readme = repository.file_contents[root_readme]

            except Exception:
                repository.readme = ""

        return repository