from core.llm.schemas import ProjectClassification

from core.scoring.domain_scores import DomainScore
from core.scoring.overall_score import OverallScore

from core.scoring.weights import (
    BASE_WEIGHTS,
    CATEGORY_OVERRIDES,
    DOMAIN_BUDGETS,
    DOMAIN_MAP,
)


class Scorer:

    def score(
        self,
        findings: list,
        classification: ProjectClassification,
    ) -> OverallScore:

        overall_score = OverallScore(

            documentation=DomainScore(
                name="Documentation",
                max_score=DOMAIN_BUDGETS["Documentation"],
                current_score=DOMAIN_BUDGETS["Documentation"],
            ),

            structure=DomainScore(
                name="Structure",
                max_score=DOMAIN_BUDGETS["Structure"],
                current_score=DOMAIN_BUDGETS["Structure"],
            ),

            code=DomainScore(
                name="Code",
                max_score=DOMAIN_BUDGETS["Code"],
                current_score=DOMAIN_BUDGETS["Code"],
            ),

            dependency=DomainScore(
                name="Dependency",
                max_score=DOMAIN_BUDGETS["Dependency"],
                current_score=DOMAIN_BUDGETS["Dependency"],
            ),

            security=DomainScore(
                name="Security",
                max_score=DOMAIN_BUDGETS["Security"],
                current_score=DOMAIN_BUDGETS["Security"],
            ),

            health=DomainScore(
                name="Health",
                max_score=DOMAIN_BUDGETS["Health"],
                current_score=DOMAIN_BUDGETS["Health"],
            ),

        )

        overrides = CATEGORY_OVERRIDES.get(
            classification.primary_category,
            {},
        )

        for finding in findings:

            weight = BASE_WEIGHTS.get(
                finding.id,
            )

            if weight is None:
                continue

            deduction = weight["deduction"]

            deduction += overrides.get(
                finding.id,
                0,
            )

            deduction = max(
                0,
                deduction,
            )

            domain = getattr(
                overall_score,
                DOMAIN_MAP[
                    weight["domain"]
                ],
            )

            domain.deduct(
                points=deduction,
                finding_id=finding.id,
                title=finding.title,
            )

        return overall_score