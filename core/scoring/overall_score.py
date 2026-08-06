from dataclasses import dataclass

from core.scoring.domain_scores import DomainScore


@dataclass
class OverallScore:

    documentation: DomainScore

    structure: DomainScore

    code: DomainScore

    dependency: DomainScore

    security: DomainScore

    health: DomainScore

    @property
    def overall_score(
        self,
    ) -> int:

        return (
            self.documentation.current_score
            + self.structure.current_score
            + self.code.current_score
            + self.dependency.current_score
            + self.security.current_score
            + self.health.current_score
        )