from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

from models.repository import Repository
from models.structure_metrics import StructureMetrics


class StructureExtractor:
    """
    Extracts deterministic repository structure metrics.

    Responsibilities:
        - Analyze directory layout
        - Detect standard project folders
        - Detect configuration files
        - Analyze naming conventions
        - Compute directory statistics

    Does NOT:
        - Produce findings
        - Score
        - Recommend
    """

    SRC_DIRECTORIES = {
        "src",
        "source",
        "app",
    }

    TEST_DIRECTORIES = {
        "test",
        "tests",
        "__tests__",
        "spec",
        "specs",
    }

    DOC_DIRECTORIES = {
        "docs",
        "doc",
    }

    ASSET_DIRECTORIES = {
        "assets",
        "asset",
        "static",
        "public",
        "images",
        "img",
    }

    SCRIPT_DIRECTORIES = {
        "scripts",
        "script",
        "tools",
    }

    CONFIG_DIRECTORIES = {
        "config",
        "configs",
        ".github",
        ".vscode",
    }

    EXAMPLE_DIRECTORIES = {
        "example",
        "examples",
        "sample",
        "samples",
    }

    BUILD_DIRECTORIES = {
        "build",
    }

    DIST_DIRECTORIES = {
        "dist",
        "distribution",
    }

    BIN_DIRECTORIES = {
        "bin",
    }

    LIB_DIRECTORIES = {
        "lib",
        "libs",
    }

    CONFIG_FILES = {
        ".gitignore": "has_gitignore",
        ".editorconfig": "has_editorconfig",
        "Dockerfile": "has_dockerfile",
        "docker-compose.yml": "has_docker_compose",
        "docker-compose.yaml": "has_docker_compose",
        "Makefile": "has_makefile",
        "package.json": "has_package_json",
        "package-lock.json": "has_package_lock",
        "yarn.lock": "has_yarn_lock",
        "pnpm-lock.yaml": "has_pnpm_lock",
        "requirements.txt": "has_requirements_txt",
        "pyproject.toml": "has_pyproject_toml",
        "poetry.lock": "has_poetry_lock",
        "Pipfile": "has_pipfile",
        "Pipfile.lock": "has_pipfile_lock",
        "Cargo.toml": "has_cargo_toml",
        "go.mod": "has_go_mod",
        "build.gradle": "has_gradle",
        "pom.xml": "has_maven",
    }

    SNAKE_CASE = re.compile(r"^[a-z]+(_[a-z0-9]+)+$")
    CAMEL_CASE = re.compile(r"^[a-z]+([A-Z][a-z0-9]*)+$")
    PASCAL_CASE = re.compile(r"^[A-Z][a-zA-Z0-9]+$")
    KEBAB_CASE = re.compile(r"^[a-z]+(-[a-z0-9]+)+$")
    UPPER_CASE = re.compile(r"^[A-Z0-9_]+$")

    def extract(self, repository: Repository) -> Repository:

        metrics = StructureMetrics()

        self._extract_directory_metrics(repository, metrics)
        self._extract_configuration_metrics(repository, metrics)
        self._extract_layout_metrics(repository, metrics)

        repository.structure_metrics = metrics

        return repository

    def _extract_directory_metrics(
        self,
        repository: Repository,
        metrics: StructureMetrics,
    ) -> None:

        directories = repository.directories

        metrics.total_directories = len(directories)

        if not directories:
            return

        depth_sum = 0

        directory_file_counter = Counter()

        directory_depths = {}

        directory_set = {
            directory.resolve()
            for directory in directories
        }

        for directory in directories:

            relative = directory.relative_to(
                repository.local_path
            )

            depth = len(relative.parts)

            directory_depths[str(relative)] = depth

            depth_sum += depth

            metrics.max_directory_depth = max(
                metrics.max_directory_depth,
                depth,
            )

            name = directory.name.lower()

            self._detect_standard_directory(
                name,
                metrics,
            )

            self._detect_directory_naming(
                directory.name,
                metrics,
            )

        for file in repository.source_files:

            parent = file.parent

            if parent.resolve() in directory_set:

                relative_parent = str(
                    parent.relative_to(repository.local_path)
                )

                directory_file_counter[
                    relative_parent
                ] += 1

            relative_file = file.relative_to(
                repository.local_path
            )

            if len(relative_file.parts) == 1:
                metrics.root_file_count += 1
            else:
                metrics.nested_file_count += 1

        metrics.directory_file_counts = dict(
            directory_file_counter
        )

        metrics.directory_depths = directory_depths

        occupied_directories = set(
            directory_file_counter.keys()
        )

        metrics.empty_directories = 0
        for directory in directories:
            try:
                if not any(directory.iterdir()):
                    metrics.empty_directories += 1
            except OSError:
                continue


        metrics.average_directory_depth = (
            depth_sum / metrics.total_directories
        )

        if metrics.total_directories:

            metrics.average_files_per_directory = (
                len(repository.source_files)
                / metrics.total_directories
            )

        if directory_file_counter:

            largest = max(
                directory_file_counter.items(),
                key=lambda item: item[1],
            )

            metrics.largest_directory = largest[0]
            metrics.largest_directory_file_count = largest[1]

    def _extract_configuration_metrics(
            self,
            repository: Repository,
            metrics: StructureMetrics,
        ) -> None:

            for filename, attribute in self.CONFIG_FILES.items():

                if self._has_config_file(
                    repository,
                    filename,
                ):
                    setattr(
                        metrics,
                        attribute,
                        True,
                    )

    def _detect_standard_directory(
        self,
        directory_name: str,
        metrics: StructureMetrics,
    ) -> None:

        if directory_name in self.SRC_DIRECTORIES:
            metrics.has_src_directory = True

        if directory_name in self.TEST_DIRECTORIES:
            metrics.has_test_directory = True

        if directory_name in self.DOC_DIRECTORIES:
            metrics.has_docs_directory = True

        if directory_name in self.ASSET_DIRECTORIES:
            metrics.has_assets_directory = True

        if directory_name in self.EXAMPLE_DIRECTORIES:
            metrics.has_examples_directory = True

        if directory_name in self.SCRIPT_DIRECTORIES:
            metrics.has_scripts_directory = True

        if directory_name in self.CONFIG_DIRECTORIES:
            metrics.has_config_directory = True

        if directory_name in self.BUILD_DIRECTORIES:
            metrics.has_build_directory = True

        if directory_name in self.DIST_DIRECTORIES:
            metrics.has_dist_directory = True

        if directory_name in self.BIN_DIRECTORIES:
            metrics.has_bin_directory = True

        if directory_name in self.LIB_DIRECTORIES:
            metrics.has_lib_directory = True

    def _detect_directory_naming(
        self,
        directory_name: str,
        metrics: StructureMetrics,
    ) -> None:

        if self.SNAKE_CASE.fullmatch(directory_name):
            metrics.snake_case_directories += 1
            return

        if self.CAMEL_CASE.fullmatch(directory_name):
            metrics.camel_case_directories += 1
            return

        if self.PASCAL_CASE.fullmatch(directory_name):
            metrics.pascal_case_directories += 1
            return

        if self.KEBAB_CASE.fullmatch(directory_name):
            metrics.kebab_case_directories += 1
            return

        if self.UPPER_CASE.fullmatch(directory_name):
            metrics.uppercase_directories += 1
            return

        metrics.mixed_case_directories += 1


    def _extract_layout_metrics(
        self,
        repository: Repository,
        metrics: StructureMetrics,
    ) -> None:

        metrics.conventional_layout = any(
            (
                metrics.has_src_directory,
                metrics.has_docs_directory,
                metrics.has_test_directory,
            )
        )

        top_level_modules = sum(
            (
                metrics.has_src_directory,
                metrics.has_lib_directory,
                metrics.has_examples_directory,
                metrics.has_scripts_directory,
            )
        )

        metrics.monorepo_detected = top_level_modules >= 3

        metrics.file_extensions = {
            extension: len(files)
            for extension, files in repository.files_by_extension.items()
        }

    @staticmethod
    def _has_config_file(
        repository: Repository,
        filename: str,
    ) -> bool:

        return any(
            path.name.lower() == filename.lower()
            for path in repository.config_files.values()
        )