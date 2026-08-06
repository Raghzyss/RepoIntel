from dataclasses import dataclass


@dataclass(slots=True)
class Finding:
    """
    Represents one engineering finding produced by the Rule Engine.
    """

    id: str
    category: str
    severity: str
    title: str
    message: str
    recommendation: str