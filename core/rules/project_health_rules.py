from models.finding import Finding
from models.project_health_metrics import ProjectHealthMetrics


class ProjectHealthRules:
    """
    Evaluates repository health metrics and produces engineering findings.
    """

    def evaluate(
        self,
        metrics: ProjectHealthMetrics,
    ) -> list[Finding]:

        findings: list[Finding] = []

        if not metrics.has_changelog:

            findings.append(
                Finding(
                    id="HLTH002",
                    category="Project Health",
                    severity="LOW",
                    title="Changelog Missing",
                    message="Repository does not contain a changelog.",
                    recommendation="Maintain a CHANGELOG.md file."
                )
            )


        if not metrics.has_code_of_conduct:

            findings.append(
                Finding(
                    id="HLTH004",
                    category="Project Health",
                    severity="LOW",
                    title="Code of Conduct Missing",
                    message="Repository does not contain a Code of Conduct.",
                    recommendation="Add a CODE_OF_CONDUCT.md file."
                )
            )


        if not metrics.has_tests:

            findings.append(
                Finding(
                    id="HLTH006",
                    category="Project Health",
                    severity="MEDIUM",
                    title="Tests Missing",
                    message="No test directory detected.",
                    recommendation="Add automated tests."
                )
            )

        if not metrics.has_github_actions:

            findings.append(
                Finding(
                    id="HLTH007",
                    category="Project Health",
                    severity="LOW",
                    title="CI Pipeline Missing",
                    message="No GitHub Actions workflow detected.",
                    recommendation="Configure a CI pipeline."
                )
            )

        if not metrics.has_dockerfile:

            findings.append(
                Finding(
                    id="HLTH008",
                    category="Project Health",
                    severity="LOW",
                    title="Dockerfile Missing",
                    message="Repository does not include a Dockerfile.",
                    recommendation="Consider adding containerization support."
                )
            )

        return findings