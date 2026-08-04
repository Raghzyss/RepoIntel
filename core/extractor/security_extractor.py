from __future__ import annotations

import re
from pathlib import Path

from models.repository import Repository
from models.security_metrics import SecurityMetrics


class SecurityExtractor:
    """
    Extracts deterministic security metrics.

    Responsibilities
    ----------------
    - Detect potential secrets
    - Detect environment files
    - Detect security documentation
    - Detect dangerous APIs
    - Produce only metrics

    Never:
    - Score
    - Produce findings
    - Recommend
    """

    AWS_KEY_PATTERN = re.compile(r"AKIA[0-9A-Z]{16}")

    GITHUB_TOKEN_PATTERN = re.compile(
        r"gh[pousr]_[A-Za-z0-9]{36,255}"
    )

    GOOGLE_API_PATTERN = re.compile(
        r"AIza[0-9A-Za-z\-_]{35}"
    )

    PRIVATE_KEY_PATTERN = re.compile(
        r"-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----"
    )

    EVAL_PATTERN = re.compile(r"\beval\s*\(")

    EXEC_PATTERN = re.compile(r"\bexec\s*\(")

    SHELL_PATTERN = re.compile(
        r"(subprocess\.|os\.system|Runtime\.getRuntime|ProcessBuilder|child_process)"
    )

    CERTIFICATE_EXTENSIONS = {
        ".crt",
        ".cer",
        ".pem",
    }

    KEY_EXTENSIONS = {
        ".key",
        ".p8",
        ".p12",
    }

    def extract(
        self,
        repository: Repository,
    ) -> Repository:

        metrics = SecurityMetrics()

        self._detect_configuration(
            repository,
            metrics,
        )

        self._scan_repository(
            repository,
            metrics,
        )

        repository.security_metrics = metrics

        return repository

    def _detect_configuration(
        self,
        repository: Repository,
        metrics: SecurityMetrics,
    ) -> None:

        config_names = {
            path.name
            for path in repository.config_files.values()
        }

        metrics.gitignore_present = (
            ".gitignore" in config_names
        )

        metrics.lock_file_present = any(
            name in config_names
            for name in (
                "package-lock.json",
                "yarn.lock",
                "pnpm-lock.yaml",
                "poetry.lock",
                "Pipfile.lock",
            )
        )

        metrics.has_security_policy = any(
            name in config_names
            for name in (
                "SECURITY.md",
                "SECURITY",
                "Security",
                "security",
            )
        )

    def _scan_repository(
        self,
        repository: Repository,
        metrics: SecurityMetrics,
    ) -> None:

        for path, content in repository.file_contents.items():

            filename = path.name.lower()

            ignored_directories = {
                "tests",
                "test",
                "examples",
                "example",
                "fixtures",
                "fixture",
                "sample",
                "samples",
            }

            is_test_or_example = any(
                part.lower() in ignored_directories
                for part in path.parts
            )

            if (
                filename == ".env"
                and not is_test_or_example
            ):
                metrics.has_env_file = True

            if (
                filename in (
                    ".env.example",
                    ".env.sample",
                    ".env.template",
                )
                and not is_test_or_example
            ):
                metrics.has_env_example = True

            self._scan_file(
                path,
                content,
                metrics,
            )

    def _scan_file(
        self,
        path: Path,
        content: str,
        metrics: SecurityMetrics,
    ) -> None:

        metrics.aws_keys += len(
            self.AWS_KEY_PATTERN.findall(content)
        )

        metrics.github_tokens += len(
            self.GITHUB_TOKEN_PATTERN.findall(content)
        )

        metrics.google_api_keys += len(
            self.GOOGLE_API_PATTERN.findall(content)
        )

        metrics.private_keys += len(
            self.PRIVATE_KEY_PATTERN.findall(content)
        )

        metrics.eval_usage += len(
            self.EVAL_PATTERN.findall(content)
        )

        metrics.exec_usage += len(
            self.EXEC_PATTERN.findall(content)
        )

        metrics.shell_execution_usage += len(
            self.SHELL_PATTERN.findall(content)
        )

        suffix = path.suffix.lower()

        if suffix in self.CERTIFICATE_EXTENSIONS:
            metrics.certificate_files += 1

        if suffix in self.KEY_EXTENSIONS:
            metrics.key_files += 1

        if suffix in (
            ".sh",
            ".bat",
            ".cmd",
            ".ps1",
        ):
            metrics.executable_scripts += 1

        metrics.potential_secrets = (
            metrics.aws_keys
            + metrics.github_tokens
            + metrics.google_api_keys
            + metrics.private_keys
        )