from models.finding import Finding
from models.repository import Repository

from core.rules.documentation_rules import DocumentationRules
from core.rules.structure_rules import StructureRules
from core.rules.code_rules import CodeRules
from core.rules.dependency_rules import DependencyRules
from core.rules.security_rules import SecurityRules
from core.rules.project_health_rules import ProjectHealthRules


class RuleEngine:
    """
    Runs all rule evaluators and produces a unified list of engineering findings.
    """

    def __init__(self) -> None:

        self.documentation_rules = DocumentationRules()
        self.structure_rules = StructureRules()
        self.code_rules = CodeRules()
        self.dependency_rules = DependencyRules()
        self.security_rules = SecurityRules()
        self.project_health_rules = ProjectHealthRules()

    def evaluate(
        self,
        repository: Repository,
    ) -> list[Finding]:

        findings: list[Finding] = []

        findings.extend(
            self.documentation_rules.evaluate(
                repository.documentation_metrics
            )
        )

        findings.extend(
            self.structure_rules.evaluate(
                repository.structure_metrics
            )
        )

        findings.extend(
            self.code_rules.evaluate(
                repository.code_metrics
            )
        )

        findings.extend(
            self.dependency_rules.evaluate(
                repository.dependency_metrics
            )
        )

        findings.extend(
            self.security_rules.evaluate(
                repository.security_metrics
            )
        )

        findings.extend(
            self.project_health_rules.evaluate(
                repository.project_health_metrics
            )
        )

        return findings