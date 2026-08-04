from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from models.documentation_metrics import DocumentationMetrics
from models.structure_metrics import StructureMetrics
from models.code_metrics import CodeMetrics
from models.dependency_metrics import DependencyMetrics
from models.security_metrics import SecurityMetrics
from models.project_health_metrics import ProjectHealthMetrics


@dataclass
class Repository:
    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------
    name: str
    owner: str
    url: str
    local_path: Path

    # ------------------------------------------------------------------
    # Documentation
    # ------------------------------------------------------------------
    readme: str = ""
    readme_path: Path | None = None

    # ------------------------------------------------------------------
    # Repository Structure
    # ------------------------------------------------------------------
    folder_tree: List[str] = field(default_factory=list)
    directories: List[Path] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Source Files
    # ------------------------------------------------------------------
    source_files: List[Path] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Fast File Access
    # ------------------------------------------------------------------
    file_contents: Dict[Path, str] = field(default_factory=dict)
    file_sizes: Dict[Path, int] = field(default_factory=dict)
    files_by_extension: Dict[str, List[Path]] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Configuration Files
    # ------------------------------------------------------------------
    config_files: Dict[str, Path] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Languages
    # ------------------------------------------------------------------
    languages: Dict[str, int] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Technology Stack
    # ------------------------------------------------------------------
    technology_stack: Dict[str, List[str]] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Repository Statistics
    # ------------------------------------------------------------------
    total_files: int = 0
    total_lines: int = 0

    # ------------------------------------------------------------------
    # Extracted Metrics
    # ------------------------------------------------------------------
    documentation_metrics: Optional[DocumentationMetrics] = None
    structure_metrics: Optional[StructureMetrics] = None
    code_metrics: Optional[CodeMetrics] = None
    dependency_metrics: Optional[DependencyMetrics] = None
    security_metrics: Optional[SecurityMetrics] = None
    project_health_metrics: Optional[ProjectHealthMetrics] = None