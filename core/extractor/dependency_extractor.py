from __future__ import annotations

import json
import re
from pathlib import Path

from models.dependency_metrics import DependencyMetrics
from models.repository import Repository


class DependencyExtractor:
    """
    Extracts deterministic dependency management metrics.

    Responsibilities
    ----------------
    - Detect package managers
    - Count dependencies
    - Detect lock files
    - Classify dependency versions

    Never:
    - Score
    - Produce findings
    - Recommend
    """

    RANGE_PREFIXES = (
        "^",
        "~",
        ">",
        "<",
        ">=",
        "<=",
    )

    def extract(
        self,
        repository: Repository,
    ) -> Repository:

        metrics = DependencyMetrics()

        self._detect_package_managers(
            repository,
            metrics,
        )

        self._parse_package_json(
            repository,
            metrics,
        )

        self._parse_requirements(
            repository,
            metrics,
        )

        self._parse_pyproject(
            repository,
            metrics,
        )

        self._detect_multiple_package_managers(
            metrics,
        )

        repository.dependency_metrics = metrics

        return repository

    def _detect_package_managers(
        self,
        repository: Repository,
        metrics: DependencyMetrics,
    ) -> None:

        configs = repository.config_files

        metrics.has_npm = "package.json" in configs
        metrics.has_pip = "requirements.txt" in configs
        metrics.has_poetry = "pyproject.toml" in configs
        metrics.has_cargo = "Cargo.toml" in configs
        metrics.has_go_modules = "go.mod" in configs
        metrics.has_gradle = (
            "build.gradle" in configs
            or "build.gradle.kts" in configs
        )
        metrics.has_maven = "pom.xml" in configs

        metrics.has_package_lock = (
            "package-lock.json" in configs
        )

        metrics.has_yarn_lock = (
            "yarn.lock" in configs
        )

        metrics.has_pnpm_lock = (
            "pnpm-lock.yaml" in configs
        )

        metrics.has_poetry_lock = (
            "poetry.lock" in configs
        )

        metrics.has_pipfile_lock = (
            "Pipfile.lock" in configs
        )

        metrics.has_yarn = metrics.has_yarn_lock
        metrics.has_pnpm = metrics.has_pnpm_lock

        metrics.has_lock_file = any(
            (
                metrics.has_package_lock,
                metrics.has_yarn_lock,
                metrics.has_pnpm_lock,
                metrics.has_poetry_lock,
                metrics.has_pipfile_lock,
            )
        )

    def _parse_package_json(
        self,
        repository: Repository,
        metrics: DependencyMetrics,
    ) -> None:

        path = repository.config_files.get(
            "package.json"
        )

        if path is None:
            return

        try:
            data = json.loads(
                repository.file_contents[path]
            )
        except Exception:
            return

        self._count_dependency_group(
            data.get("dependencies", {}),
            metrics,
            "production",
        )

        self._count_dependency_group(
            data.get("devDependencies", {}),
            metrics,
            "development",
        )

        self._count_dependency_group(
            data.get("peerDependencies", {}),
            metrics,
            "peer",
        )

        self._count_dependency_group(
            data.get("optionalDependencies", {}),
            metrics,
            "optional",
        )

    def _parse_requirements(
        self,
        repository: Repository,
        metrics: DependencyMetrics,
    ) -> None:

        path = repository.config_files.get(
            "requirements.txt"
        )

        if path is None:
            return

        for line in repository.file_contents[
            path
        ].splitlines():

            line = line.strip()

            if (
                not line
                or line.startswith("#")
            ):
                continue

            metrics.total_dependencies += 1
            metrics.production_dependencies += 1

            self._classify_version(
                line,
                metrics,
            )

    def _parse_pyproject(
        self,
        repository: Repository,
        metrics: DependencyMetrics,
    ) -> None:

        path = repository.config_files.get(
            "pyproject.toml"
        )

        if path is None:
            return

        text = repository.file_contents[path]

        dependency_lines = re.findall(
            r'^\s*([A-Za-z0-9_.-]+)\s*=',
            text,
            flags=re.MULTILINE,
        )

        for dependency in dependency_lines:

            if dependency in (
                "python",
                "name",
                "version",
                "description",
            ):
                continue

            metrics.total_dependencies += 1
            metrics.production_dependencies += 1

            self._classify_version(
                dependency,
                metrics,
            )

    def _count_dependency_group(
        self,
        dependencies: dict,
        metrics: DependencyMetrics,
        dependency_type: str,
    ) -> None:

        if not isinstance(dependencies, dict):
            return

        for _, version in dependencies.items():

            metrics.total_dependencies += 1

            if dependency_type == "production":
                metrics.production_dependencies += 1

            elif dependency_type == "development":
                metrics.development_dependencies += 1

            elif dependency_type == "peer":
                metrics.peer_dependencies += 1

            elif dependency_type == "optional":
                metrics.optional_dependencies += 1

            self._classify_version(
                str(version),
                metrics,
            )

    def _classify_version(
        self,
        version: str,
        metrics: DependencyMetrics,
    ) -> None:

        version = version.strip()

        if version in (
            "*",
            "latest",
            "",
        ):
            metrics.latest_dependencies += 1
            return

        if version.startswith(self.RANGE_PREFIXES):
            metrics.ranged_dependencies += 1
            return

        if any(
            operator in version
            for operator in (
                ">",
                "<",
                "~",
                "^",
                "*",
            )
        ):
            metrics.ranged_dependencies += 1
            return

        metrics.pinned_dependencies += 1

    def _detect_multiple_package_managers(
        self,
        metrics: DependencyMetrics,
    ) -> None:

        managers = sum(
            (
                metrics.has_npm,
                metrics.has_yarn,
                metrics.has_pnpm,
                metrics.has_pip,
                metrics.has_poetry,
                metrics.has_cargo,
                metrics.has_gradle,
                metrics.has_maven,
                metrics.has_go_modules,
            )
        )

        metrics.multiple_package_managers = managers > 1