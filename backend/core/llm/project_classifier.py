import json

from models.repository import Repository

from core.llm.gemini_client import GeminiClient
from core.llm.prompts import PROJECT_CLASSIFICATION_PROMPT
from core.llm.schemas import ProjectClassification


class ProjectClassifier:

    def __init__(self):

        self.client = GeminiClient()

    def classify(
        self,
        repository: Repository,
    ) -> ProjectClassification:

        summary = self._build_repository_summary(
            repository,
        )

        prompt = PROJECT_CLASSIFICATION_PROMPT.format(
            repository_summary=summary,
        )

        response = self.client.generate(
            prompt,
        )

        try:

            data = json.loads(
                response,
            )

            confidence = data.get(
                "confidence",
                0,
            )

            if isinstance(
                confidence,
                float,
            ) and confidence <= 1:

                confidence = round(
                    confidence * 100
                )

            else:

                confidence = round(
                    confidence
                )

            return ProjectClassification(
                primary_category=data.get(
                    "primary_category",
                    "UNKNOWN",
                ),
                secondary_category=data.get(
                    "secondary_category",
                ),
                confidence=confidence,
                repository_purpose=data.get(
                    "repository_purpose",
                    "",
                ),
                maturity=data.get(
                    "maturity",
                    "PROTOTYPE",
                ),
                raw_response=response,
            )

        except Exception:

            return ProjectClassification(
                primary_category="UNKNOWN",
                secondary_category=None,
                confidence=0,
                repository_purpose="",
                maturity="PROTOTYPE",
                raw_response=response,
            )

    def _build_repository_summary(
        self,
        repository: Repository,
    ) -> str:

        summary = []

        summary.append(
            f"Repository Name: {repository.name}"
        )

        summary.append(
            f"Owner: {repository.owner}"
        )

        summary.append(
            f"Languages: {repository.languages}"
        )

        summary.append(
            f"Technology Stack: {repository.technology_stack}"
        )

        summary.append(
            f"Total Files: {repository.total_files}"
        )

        summary.append(
            f"Total Lines: {repository.total_lines}"
        )

        summary.append(
            "Configuration Files:"
        )

        for config in repository.config_files.keys():

            summary.append(
                f"- {config}"
            )

        summary.append(
            "README:"
        )

        summary.append(
            repository.readme[:4000]
        )

        return "\n".join(
            summary,
        )