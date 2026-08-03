from pathlib import Path


LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SASS",
    ".json": "JSON",
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".sql": "SQL",
    ".sh": "Shell",
}


class LanguageDetector:

    def detect(self, repository):

        repository.languages.clear()

        for file in repository.source_files:

            extension = Path(file).suffix.lower()

            language = LANGUAGE_MAP.get(extension)

            if language is None:
                continue

            repository.languages[language] = (
                repository.languages.get(language, 0) + 1
            )

        return repository