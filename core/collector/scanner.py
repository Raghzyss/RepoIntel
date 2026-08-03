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
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "dockerfile",
    "docker-compose.yml",
    "pom.xml",
    "build.gradle",
    "pyproject.toml",
    "tsconfig.json",
    "next.config.js",
    "next.config.ts",
    "next.config.mjs",
    "vite.config.js",
    "vite.config.ts",
    "vite.config.mjs",
    "tailwind.config.js",
    "tailwind.config.ts",
    "tailwind.config.mjs",
}


class RepositoryScanner:

    def scan(self, repository):

        root_readme = None

        for path in repository.local_path.rglob("*"):

            if any(part in IGNORE_DIRS for part in path.parts):
                continue

            relative_path = path.relative_to(repository.local_path)

            repository.folder_tree.append(str(relative_path))

            if not path.is_file():
                continue

            repository.total_files += 1

            # Count lines
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    repository.total_lines += sum(1 for _ in file)
            except Exception:
                pass

            # Source files
            if path.suffix.lower() in SOURCE_EXTENSIONS:
                repository.source_files.append(path)

            filename = path.name.lower()

            # Config files
            if filename in CONFIG_FILES:
                repository.config_files[filename] = path

            # README detection
            if filename.startswith("readme"):

                # Prefer repository root README
                if path.parent == repository.local_path:
                    root_readme = path

                elif root_readme is None:
                    root_readme = path

        # Read README once after scanning
        if root_readme:

            try:
                repository.readme = root_readme.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except Exception:
                pass

        return repository