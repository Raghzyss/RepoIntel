from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class Repository:
    # Basic Information
    name: str
    owner: str
    url: str
    local_path: Path

    # Content
    readme: str = ""

    # Structure
    folder_tree: List[str] = field(default_factory=list)

    # Files
    source_files: List[Path] = field(default_factory=list)

    # Configuration Files
    config_files: Dict[str, Path] = field(default_factory=dict)

    # Languages
    languages: Dict[str, int] = field(default_factory=dict)

    # Technology Stack
    technology_stack: Dict[str, List[str]] = field(default_factory=dict)

    # Statistics
    total_files: int = 0
    total_lines: int = 0