from dataclasses import dataclass


@dataclass(slots=True)
class SecurityMetrics:
    """
    Stores deterministic repository security metrics.

    Contains only measurable values.
    """

    # ----------------------------------------------------------
    # Secrets
    # ----------------------------------------------------------

    potential_secrets: int = 0

    aws_keys: int = 0
    github_tokens: int = 0
    google_api_keys: int = 0
    private_keys: int = 0

    # ----------------------------------------------------------
    # Environment Files
    # ----------------------------------------------------------

    has_env_file: bool = False
    has_env_example: bool = False

    # ----------------------------------------------------------
    # Security Documentation
    # ----------------------------------------------------------

    has_security_policy: bool = False

    # ----------------------------------------------------------
    # Dependency Security
    # ----------------------------------------------------------

    lock_file_present: bool = False

    # ----------------------------------------------------------
    # Dangerous Files
    # ----------------------------------------------------------

    executable_scripts: int = 0

    # ----------------------------------------------------------
    # Repository Configuration
    # ----------------------------------------------------------

    gitignore_present: bool = False

    # ----------------------------------------------------------
    # Certificates / Keys
    # ----------------------------------------------------------

    certificate_files: int = 0
    key_files: int = 0

    # ----------------------------------------------------------
    # Dangerous Patterns
    # ----------------------------------------------------------

    eval_usage: int = 0
    exec_usage: int = 0
    shell_execution_usage: int = 0