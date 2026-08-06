from models.documentation_metrics import DocumentationMetrics
from models.finding import Finding


class DocumentationRules:

    def evaluate(
        self,
        metrics: DocumentationMetrics,
    ) -> list[Finding]:

        findings = []

        if not metrics.readme_exists:

            findings.append(
                Finding(
                    id="DOC001",
                    category="Documentation",
                    severity="HIGH",
                    title="README Missing",
                    message="Repository does not contain a README file.",
                    recommendation="Add a README explaining the project.",
                )
            )

            return findings

        if metrics.readme_word_count < 100:

            findings.append(
                Finding(
                    id="DOC002",
                    category="Documentation",
                    severity="MEDIUM",
                    title="README Too Small",
                    message="README contains very little documentation.",
                    recommendation="Expand the README with setup and usage instructions.",
                )
            )

        if (
            not metrics.has_installation_section
            and not metrics.has_examples_section
        ):

            findings.append(
                Finding(
                    id="DOC003",
                    category="Documentation",
                    severity="MEDIUM",
                    title="Installation Section Missing",
                    message="README does not explain installation.",
                    recommendation="Add an Installation section or provide installation examples.",
                )
            )

        if (
            not metrics.has_usage_section
            and not metrics.has_examples_section
        ):

            findings.append(
                Finding(
                    id="DOC004",
                    category="Documentation",
                    severity="MEDIUM",
                    title="Usage Section Missing",
                    message="README does not explain how to use the project.",
                    recommendation="Add a Usage section or provide practical examples.",
                )
            )

        if not metrics.has_license_file:

            findings.append(
                Finding(
                    id="DOC005",
                    category="Documentation",
                    severity="LOW",
                    title="License Missing",
                    message="Repository does not contain a LICENSE file.",
                    recommendation="Add an open-source license.",
                )
            )

        if metrics.badge_count == 0:

            findings.append(
                Finding(
                    id="DOC006",
                    category="Documentation",
                    severity="LOW",
                    title="No README Badges",
                    message="README does not contain any status badges.",
                    recommendation="Consider adding build, version, coverage or license badges.",
                )
            )

        if (
            not metrics.has_contributing_file
            and not metrics.has_contributing_section
        ):

            findings.append(
                Finding(
                    id="DOC007",
                    category="Documentation",
                    severity="LOW",
                    title="Contributing Guide Missing",
                    message="Repository does not provide contribution guidelines.",
                    recommendation="Provide contribution guidelines through a CONTRIBUTING.md file or a dedicated README section.",
                )
            )

        return findings