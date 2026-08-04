from dataclasses import dataclass, field


@dataclass(slots=True)
class StructureMetrics:
    """
    Stores deterministic repository structure metrics.

    Contains only measurable values.
    No findings.
    No scores.
    No recommendations.
    """

    # ------------------------------------------------------------------
    # Repository Structure
    # ------------------------------------------------------------------

    total_directories: int = 0
    empty_directories: int = 0
    max_directory_depth: int = 0
    average_directory_depth: float = 0.0

    root_file_count: int = 0
    nested_file_count: int = 0

    largest_directory: str = ""
    largest_directory_file_count: int = 0

    average_files_per_directory: float = 0.0

    # ------------------------------------------------------------------
    # Standard Project Directories
    # ------------------------------------------------------------------

    has_src_directory: bool = False
    has_test_directory: bool = False
    has_docs_directory: bool = False
    has_assets_directory: bool = False
    has_examples_directory: bool = False
    has_scripts_directory: bool = False
    has_config_directory: bool = False

    # ------------------------------------------------------------------
    # Build / Distribution
    # ------------------------------------------------------------------

    has_build_directory: bool = False
    has_dist_directory: bool = False
    has_bin_directory: bool = False
    has_lib_directory: bool = False

    # ------------------------------------------------------------------
    # Naming Conventions
    # ------------------------------------------------------------------

    snake_case_directories: int = 0
    camel_case_directories: int = 0
    pascal_case_directories: int = 0
    kebab_case_directories: int = 0
    uppercase_directories: int = 0
    mixed_case_directories: int = 0

    # ------------------------------------------------------------------
    # Layout Detection
    # ------------------------------------------------------------------

    conventional_layout: bool = False
    monorepo_detected: bool = False

    # ------------------------------------------------------------------
    # Configuration Files
    # ------------------------------------------------------------------

    has_gitignore: bool = False
    has_editorconfig: bool = False
    has_dockerfile: bool = False
    has_docker_compose: bool = False
    has_makefile: bool = False

    has_package_json: bool = False
    has_package_lock: bool = False
    has_yarn_lock: bool = False
    has_pnpm_lock: bool = False

    has_requirements_txt: bool = False
    has_pyproject_toml: bool = False
    has_poetry_lock: bool = False
    has_pipfile: bool = False
    has_pipfile_lock: bool = False

    has_cargo_toml: bool = False
    has_go_mod: bool = False
    has_gradle: bool = False
    has_maven: bool = False

    # ------------------------------------------------------------------
    # Extension Distribution
    # ------------------------------------------------------------------

    file_extensions: dict[str, int] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Directory Statistics
    # ------------------------------------------------------------------

    directory_file_counts: dict[str, int] = field(default_factory=dict)
    directory_depths: dict[str, int] = field(default_factory=dict)