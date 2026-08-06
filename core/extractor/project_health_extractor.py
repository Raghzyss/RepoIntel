from __future__ import annotations

from models.project_health_metrics import ProjectHealthMetrics
from models.repository import Repository


class ProjectHealthExtractor:
    """
    Extracts deterministic project health metrics.

    Responsibilities
    ----------------
    - Detect health-related repository artifacts
    - Detect CI/CD
    - Detect testing structure
    - Produce only metrics

    Never:
    - Score
    - Produce findings
    - Recommend
    """

    TEST_DIRECTORIES = {
        "test",
        "tests",
        "__tests__",
        "spec",
        "specs",
    }

    def extract(
        self,
        repository: Repository,
    ) -> Repository:

        metrics = ProjectHealthMetrics()

        config_names = {
            path.name
            for path in repository.config_files.values()
        }

        metrics.has_readme = bool(repository.readme)


        metrics.has_changelog = any(
            name in config_names
            for name in (
                "CHANGELOG.md",
                "CHANGELOG",
                "HISTORY.md",
            )
        )


        metrics.has_code_of_conduct = any(
            name in config_names
            for name in (
                "CODE_OF_CONDUCT.md",
                "CODE_OF_CONDUCT",
            )
        )


        metrics.has_gitignore = (
            ".gitignore" in config_names
        )

        metrics.has_editorconfig = (
            ".editorconfig" in config_names
        )

        metrics.has_makefile = (
            "Makefile" in config_names
        )

        metrics.has_dockerfile = (
            "Dockerfile" in config_names
        )

        metrics.has_docker_compose = any(
            name in config_names
            for name in (
                "docker-compose.yml",
                "docker-compose.yaml",
            )
        )

        metrics.has_github_actions = any(
            ".github/workflows" in str(directory)
            for directory in repository.directories
        )

        metrics.has_gitlab_ci = (
            ".gitlab-ci.yml" in config_names
        )

        metrics.has_circle_ci = (
            ".circleci" in {
                directory.name
                for directory in repository.directories
            }
        )

        metrics.has_travis_ci = (
            ".travis.yml" in config_names
        )

        metrics.test_directory_count = sum(
            1
            for directory in repository.directories
            if directory.name.lower()
            in self.TEST_DIRECTORIES
        )

        metrics.has_tests = (
            metrics.test_directory_count > 0
        )

        metrics.has_docs_directory = any(
            directory.name.lower() == "docs"
            for directory in repository.directories
        )

        metrics.total_files = repository.total_files
        metrics.total_directories = len(
            repository.directories
        )

        repository.project_health_metrics = metrics

        return repository