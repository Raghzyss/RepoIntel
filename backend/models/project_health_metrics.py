from dataclasses import dataclass


@dataclass(slots=True)
class ProjectHealthMetrics:
    """
    Stores deterministic project health metrics.

    Contains only measurable values.
    """

    # ----------------------------------------------------------
    # Repository Metadata
    # ----------------------------------------------------------

    has_readme: bool = False
    has_changelog: bool = False
    has_code_of_conduct: bool = False


    # ----------------------------------------------------------
    # Documentation
    # ----------------------------------------------------------

    has_docs_directory: bool = False

    # ----------------------------------------------------------
    # CI / CD
    # ----------------------------------------------------------

    has_github_actions: bool = False
    has_gitlab_ci: bool = False
    has_circle_ci: bool = False
    has_travis_ci: bool = False

    # ----------------------------------------------------------
    # Containerization
    # ----------------------------------------------------------

    has_dockerfile: bool = False
    has_docker_compose: bool = False

    # ----------------------------------------------------------
    # Testing
    # ----------------------------------------------------------

    has_tests: bool = False
    test_directory_count: int = 0

    # ----------------------------------------------------------
    # Build / Automation
    # ----------------------------------------------------------

    has_makefile: bool = False

    # ----------------------------------------------------------
    # Version Control
    # ----------------------------------------------------------

    has_gitignore: bool = False
    has_editorconfig: bool = False

    # ----------------------------------------------------------
    # Repository Size
    # ----------------------------------------------------------

    total_files: int = 0
    total_directories: int = 0