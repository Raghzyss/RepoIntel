from models.dependency_metrics import DependencyMetrics
from models.finding import Finding


class DependencyRules:
    """
    Evaluates dependency management metrics and produces engineering findings.
    """

    def evaluate(
        self,
        metrics: DependencyMetrics,
    ) -> list[Finding]:

        findings: list[Finding] = []

        if metrics.total_dependencies == 0:

            findings.append(
                Finding(
                    id="DEP001",
                    category="Dependency Management",
                    severity="LOW",
                    title="No Dependencies Detected",
                    message="No project dependencies were detected.",
                    recommendation="Ensure dependency configuration files are present if external libraries are used."
                )
            )

            return findings

        if (
            metrics.has_npm
            and not (
                metrics.has_package_lock
                or metrics.has_yarn_lock
                or metrics.has_pnpm_lock
            )
        ):

            findings.append(
                Finding(
                    id="DEP002",
                    category="Dependency Management",
                    severity="HIGH",
                    title="Lock File Missing",
                    message="No dependency lock file was detected.",
                    recommendation="Commit the appropriate lock file to ensure reproducible builds."
                )
            )

        if metrics.latest_dependencies > 0:

            findings.append(
                Finding(
                    id="DEP004",
                    category="Dependency Management",
                    severity="MEDIUM",
                    title="Unpinned Dependency Versions",
                    message=f"{metrics.latest_dependencies} dependencies use 'latest' or wildcard versions.",
                    recommendation="Pin dependency versions for reproducible builds."
                )
            )

        if metrics.ranged_dependencies > metrics.pinned_dependencies:

            findings.append(
                Finding(
                    id="DEP005",
                    category="Dependency Management",
                    severity="LOW",
                    title="Many Version Ranges",
                    message=f"{metrics.ranged_dependencies} dependencies use version ranges.",
                    recommendation="Consider pinning critical dependencies."
                )
            )

        return findings