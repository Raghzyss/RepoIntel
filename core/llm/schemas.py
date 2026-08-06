from dataclasses import dataclass
from typing import Optional
@dataclass
class ProjectClassification:
    primary_category: str
    secondary_category: Optional[str]
    confidence: int
    repository_purpose: str
    maturity: str
    raw_response: str = ""