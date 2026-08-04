from dataclasses import dataclass


@dataclass(slots=True)
class DependencyMetrics:
    """
    Stores deterministic dependency management metrics.

    Contains only measurable values.
    """

    # ----------------------------------------------------------
    # Package Managers
    # ----------------------------------------------------------

    has_npm: bool = False
    has_yarn: bool = False
    has_pnpm: bool = False
    has_pip: bool = False
    has_poetry: bool = False
    has_cargo: bool = False
    has_gradle: bool = False
    has_maven: bool = False
    has_go_modules: bool = False

    # ----------------------------------------------------------
    # Dependency Counts
    # ----------------------------------------------------------

    total_dependencies: int = 0
    production_dependencies: int = 0
    development_dependencies: int = 0
    optional_dependencies: int = 0
    peer_dependencies: int = 0

    # ----------------------------------------------------------
    # Lock Files
    # ----------------------------------------------------------

    has_lock_file: bool = False

    has_package_lock: bool = False
    has_yarn_lock: bool = False
    has_pnpm_lock: bool = False
    has_poetry_lock: bool = False
    has_pipfile_lock: bool = False

    # ----------------------------------------------------------
    # Version Information
    # ----------------------------------------------------------

    pinned_dependencies: int = 0
    ranged_dependencies: int = 0
    latest_dependencies: int = 0

    # ----------------------------------------------------------
    # Configuration
    # ----------------------------------------------------------

    multiple_package_managers: bool = False