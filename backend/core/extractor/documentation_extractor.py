from __future__ import annotations

import re
from pathlib import Path

from models.repository import Repository
from models.documentation_metrics import DocumentationMetrics


class DocumentationExtractor:
    """
    Extracts deterministic documentation metrics from a repository.

    Responsibilities:
        - Parse README
        - Detect documentation sections
        - Count markdown elements
        - Detect documentation files
        - Populate DocumentationMetrics

    Does NOT:
        - Produce findings
        - Score
        - Recommend
    """

    SECTION_KEYWORDS = {
        "installation": [
            "installation",
            "install",
            "installing",
            "getting started",
            "getting-started",
            "quick start",
            "quickstart",
            "setup",
            "set up",
            "requirements",
            "prerequisites",
        ],
        "usage": [
            "usage",
            "how to use",
            "quick start",
            "quickstart",
            "running",
            "getting started",
            "run",
            "example",
            "examples",
            "demo",
            "first steps",
            "installation and usage",
        ],
        "configuration": [
            "configuration",
            "config",
            "settings",
            "environment",
        ],
        "features": [
            "features",
            "feature",
        ],
        "examples": [
            "examples",
            "example",
            "demo",
        ],
        "api": [
            "api",
            "reference",
            "documentation",
        ],
        "testing": [
            "testing",
            "tests",
            "test",
        ],
        "contributing": [
            "contributing",
            "contribution",
        ],
        "license": [
            "license",
            "licence",
        ],
        "changelog": [
            "changelog",
            "release notes",
            "history",
        ],
        "faq": [
            "faq",
            "questions",
            "frequently asked questions",
        ],
        "support": [
            "support",
            "help",
            "contact",
        ],
        "acknowledgements": [
            "acknowledgements",
            "acknowledgments",
            "credits",
        ],
        "roadmap": [
            "roadmap",
            "future work",
            "future plans",
        ],
        "toc": [
            "table of contents",
            "contents",
        ],
    }

    LICENSE_FILES = {
        "LICENSE",
        "LICENSE.md",
        "LICENSE.txt",
        "LICENCE",
        "LICENCE.md",
    }

    CHANGELOG_FILES = {
        "CHANGELOG",
        "CHANGELOG.md",
        "HISTORY.md",
        "RELEASES.md",
    }

    CONTRIBUTING_FILES = {
        "CONTRIBUTING",
        "CONTRIBUTING.md",
    }

    CODE_OF_CONDUCT_FILES = {
        "CODE_OF_CONDUCT.md",
        "CODE_OF_CONDUCT",
    }

    SECURITY_FILES = {
        "SECURITY.md",
        "SECURITY",
    }

    AUTHORS_FILES = {
        "AUTHORS",
        "AUTHORS.md",
    }

    CITATION_FILES = {
        "CITATION.cff",
        "CITATION",
        "CITATION.md",
    }

    MARKDOWN_EXTENSIONS = {
        ".md",
        ".markdown",
        ".mdown",
    }

    TEXT_EXTENSIONS = {
        ".txt",
        ".rst",
        ".adoc",
    }

    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)

    LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    IMAGE_PATTERN = re.compile(r"!\[[^\]]*]\((.*?)\)")

    INLINE_CODE_PATTERN = re.compile(r"`[^`\n]+`")

    CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```")

    TABLE_PATTERN = re.compile(r"^\|.*\|$", re.MULTILINE)

    BLOCKQUOTE_PATTERN = re.compile(r"^>", re.MULTILINE)

    HR_PATTERN = re.compile(r"^\s*([-*_]){3,}\s*$", re.MULTILINE)

    HTML_PATTERN = re.compile(r"<[^>]+>")

    MERMAID_PATTERN = re.compile(r"```mermaid", re.IGNORECASE)

    LATEX_PATTERN = re.compile(
        r"\$\$[\s\S]*?\$\$|\\\(|\\\)|\\\[|\\\]",
        re.MULTILINE,
    )

    def extract(self, repository: Repository) -> Repository:
        metrics = DocumentationMetrics()

        self._extract_readme_metrics(repository, metrics)
        self._extract_documentation_files(repository, metrics)

        repository.documentation_metrics = metrics

        return repository

    def _extract_readme_metrics(
        self,
        repository: Repository,
        metrics: DocumentationMetrics,
    ) -> None:

        readme = repository.readme

        if not readme:
            return

        metrics.readme_exists = True

        if repository.readme_path is not None:
            metrics.readme_path = str(repository.readme_path)

        metrics.readme_character_count = len(readme)
        metrics.readme_word_count = len(readme.split())
        metrics.readme_line_count = len(readme.splitlines())
        metrics.readme_size_bytes = len(readme.encode("utf-8"))

        self._extract_headings(readme, metrics)
        self._extract_markdown_elements(readme, metrics)
        self._extract_links(readme, metrics)
        self._extract_sections(readme, metrics)

        metrics.contains_html = bool(
            self.HTML_PATTERN.search(readme)
        )

        metrics.contains_mermaid_diagrams = bool(
            self.MERMAID_PATTERN.search(readme)
        )

        metrics.contains_latex = bool(
            self.LATEX_PATTERN.search(readme)
        )

        metrics.mentions_github_wiki = (
            "wiki" in readme.lower()
        )

    def _extract_headings(
        self,
        markdown: str,
        metrics: DocumentationMetrics,
    ) -> None:

        headings = self.HEADING_PATTERN.findall(markdown)

        metrics.heading_count = len(headings)

        if not headings:
            return

        level_counts = {}

        for hashes, _ in headings:
            level = len(hashes)

            level_counts[level] = (
                level_counts.get(level, 0) + 1
            )

        metrics.heading_levels = level_counts
        metrics.max_heading_depth = max(level_counts)

        first_heading = headings[0][1].strip()

        metrics.has_title = bool(first_heading)

        if metrics.readme_word_count > 30:
            metrics.has_description = True

    def _extract_markdown_elements(
        self,
        markdown: str,
        metrics: DocumentationMetrics,
    ) -> None:

        metrics.code_block_count = len(
            self.CODE_BLOCK_PATTERN.findall(markdown)
        )

        metrics.inline_code_count = len(
            self.INLINE_CODE_PATTERN.findall(markdown)
        )

        metrics.image_count = len(
            self.IMAGE_PATTERN.findall(markdown)
        )

        metrics.table_count = len(
            self.TABLE_PATTERN.findall(markdown)
        )

        metrics.blockquote_count = len(
            self.BLOCKQUOTE_PATTERN.findall(markdown)
        )

        metrics.horizontal_rule_count = len(
            self.HR_PATTERN.findall(markdown)
        )

        metrics.list_count = sum(
            1
            for line in markdown.splitlines()
            if line.lstrip().startswith(
                ("- ", "* ", "+ ")
            )
            or re.match(r"^\d+\.", line.strip())
        )

        markdown_badges = sum(
            1
            for image in self.IMAGE_PATTERN.findall(markdown)
            if (
                "shields.io" in image.lower()
                or "badge" in image.lower()
            )
        )

        html_badges = len(
            re.findall(
                r"<img\s+[^>]*src=",
                markdown,
                flags=re.IGNORECASE,
            )
        )

        metrics.badge_count = (
            markdown_badges
            + html_badges
        )

    def _extract_links(
        self,
        markdown: str,
        metrics: DocumentationMetrics,
    ) -> None:

        links = self.LINK_PATTERN.findall(markdown)

        metrics.total_link_count = len(links)

        for _, url in links:

            lower_url = url.lower()

            if lower_url.startswith(("http://", "https://")):
                metrics.external_link_count += 1

            elif lower_url.startswith("#"):
                metrics.internal_link_count += 1

            else:
                metrics.relative_link_count += 1

    def _extract_sections(
        self,
        markdown: str,
        metrics: DocumentationMetrics,
    ) -> None:

        headings = [
            title.strip().lower()
            for _, title in self.HEADING_PATTERN.findall(markdown)
        ]

        for heading in headings:

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["installation"],
            ):
                metrics.has_installation_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["usage"],
            ):
                metrics.has_usage_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["configuration"],
            ):
                metrics.has_configuration_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["features"],
            ):
                metrics.has_features_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["examples"],
            ):
                metrics.has_examples_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["api"],
            ):
                metrics.has_api_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["testing"],
            ):
                metrics.has_testing_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["contributing"],
            ):
                metrics.has_contributing_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["license"],
            ):
                metrics.has_license_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["changelog"],
            ):
                metrics.has_changelog_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["faq"],
            ):
                metrics.has_faq_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["support"],
            ):
                metrics.has_support_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["acknowledgements"],
            ):
                metrics.has_acknowledgements_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["roadmap"],
            ):
                metrics.has_roadmap_section = True

            if self._matches_keywords(
                heading,
                self.SECTION_KEYWORDS["toc"],
            ):
                metrics.has_table_of_contents = True

    def _extract_documentation_files(
        self,
        repository: Repository,
        metrics: DocumentationMetrics,
    ) -> None:

        markdown_count = 0
        text_count = 0

        for path in repository.file_contents.keys():

            name = path.name
            suffix = path.suffix.lower()

            if suffix in self.MARKDOWN_EXTENSIONS:
                markdown_count += 1

            if suffix in self.TEXT_EXTENSIONS:
                text_count += 1

            if "docs" in {
                part.lower()
                for part in path.parts
            }:
                metrics.has_docs_directory = True

            if name in self.LICENSE_FILES:
                metrics.has_license_file = True
                metrics.license_file_name = name

            if name in self.CHANGELOG_FILES:
                metrics.has_changelog_file = True
                metrics.changelog_file_name = name

            if name in self.CONTRIBUTING_FILES:
                metrics.has_contributing_file = True
                metrics.contributing_file_name = name

            if name in self.CODE_OF_CONDUCT_FILES:
                metrics.has_code_of_conduct = True
                metrics.code_of_conduct_file_name = name

            if name in self.SECURITY_FILES:
                metrics.has_security_file = True
                metrics.security_file_name = name

            if name in self.AUTHORS_FILES:
                metrics.has_authors_file = True
                metrics.authors_file_name = name

            if name in self.CITATION_FILES:
                metrics.has_citation_file = True
                metrics.citation_file_name = name

        metrics.markdown_file_count = markdown_count
        metrics.text_document_count = text_count

        metrics.documentation_file_count = (
            markdown_count
            + text_count
            + int(metrics.has_license_file)
            + int(metrics.has_changelog_file)
            + int(metrics.has_contributing_file)
            + int(metrics.has_code_of_conduct)
            + int(metrics.has_security_file)
            + int(metrics.has_authors_file)
            + int(metrics.has_citation_file)
        )

    @staticmethod
    def _matches_keywords(
        heading: str,
        keywords: list[str],
    ) -> bool:

        heading = heading.strip().lower()

        return any(
            keyword.lower() in heading
            for keyword in keywords
        )