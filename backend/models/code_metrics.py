from dataclasses import dataclass, field


@dataclass(slots=True)
class CodeMetrics:
    """
    Stores deterministic source code metrics extracted from a repository.

    This class contains only measurable values.
    It never stores findings, scores, or recommendations.
    """

    # ------------------------------------------------------------------
    # Source Files
    # ------------------------------------------------------------------

    total_source_files: int = 0
    total_source_lines: int = 0

    largest_file: str = ""
    largest_file_lines: int = 0

    smallest_file: str = ""
    smallest_file_lines: int = 0

    average_lines_per_file: float = 0.0

    # ------------------------------------------------------------------
    # Line Statistics
    # ------------------------------------------------------------------

    code_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0

    code_line_percentage: float = 0.0
    blank_line_percentage: float = 0.0
    comment_line_percentage: float = 0.0

    # ------------------------------------------------------------------
    # File Size Distribution
    # ------------------------------------------------------------------

    files_under_100_lines: int = 0
    files_100_to_300_lines: int = 0
    files_300_to_500_lines: int = 0
    files_over_500_lines: int = 0
    files_over_1000_lines: int = 0

    # ------------------------------------------------------------------
    # Code Elements
    # ------------------------------------------------------------------

    total_classes: int = 0
    total_functions: int = 0
    total_interfaces: int = 0
    total_enums: int = 0

    # ------------------------------------------------------------------
    # Documentation Inside Code
    # ------------------------------------------------------------------

    docstring_count: int = 0
    documentation_comment_blocks: int = 0

    # ------------------------------------------------------------------
    # Comment Quality
    # ------------------------------------------------------------------

    todo_count: int = 0
    fixme_count: int = 0
    hack_count: int = 0
    xxx_count: int = 0

    # ------------------------------------------------------------------
    # File Naming
    # ------------------------------------------------------------------

    duplicate_file_names: int = 0
    duplicate_file_name_list: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Generated / Vendor Files
    # ------------------------------------------------------------------

    generated_files: int = 0
    minified_files: int = 0

    # ------------------------------------------------------------------
    # Extension Statistics
    # ------------------------------------------------------------------

    source_file_extensions: dict[str, int] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Per File Statistics
    # ------------------------------------------------------------------

    file_line_counts: dict[str, int] = field(default_factory=dict)

    file_comment_counts: dict[str, int] = field(default_factory=dict)

    file_function_counts: dict[str, int] = field(default_factory=dict)

    file_class_counts: dict[str, int] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Language Distribution
    # ------------------------------------------------------------------

    language_file_counts: dict[str, int] = field(default_factory=dict)

    language_line_counts: dict[str, int] = field(default_factory=dict)