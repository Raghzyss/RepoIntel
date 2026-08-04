from models.finding import Finding
from models.structure_metrics import StructureMetrics


class StructureRules:
    """
    Evaluates repository structure metrics and produces engineering findings.
    """

    def evaluate(
        self,
        metrics: StructureMetrics,
    ) -> list[Finding]:

        findings: list[Finding] = []

        if metrics.total_directories == 0:

            findings.append(
                Finding(
                    id="STR001",
                    category="Structure",
                    severity="HIGH",
                    title="No Directory Structure",
                    message="Repository does not contain any directories.",
                    recommendation="Organize the project into logical directories."
                )
            )

            return findings

        if metrics.max_directory_depth > 8:

            findings.append(
                Finding(
                    id="STR002",
                    category="Structure",
                    severity="MEDIUM",
                    title="Deep Directory Nesting",
                    message=f"Maximum directory depth is {metrics.max_directory_depth}.",
                    recommendation="Reduce unnecessary nesting to improve maintainability."
                )
            )

        if metrics.empty_directories > 5:

            findings.append(
                Finding(
                    id="STR003",
                    category="Structure",
                    severity="LOW",
                    title="Many Empty Directories",
                    message=f"Repository contains {metrics.empty_directories} empty directories.",
                    recommendation="Remove unused directories."
                )
            )

        if not metrics.has_src_directory:

            findings.append(
                Finding(
                    id="STR004",
                    category="Structure",
                    severity="LOW",
                    title="Source Directory Missing",
                    message="Standard source directory was not detected.",
                    recommendation="Consider placing source code inside a src/ directory."
                )
            )

        if not metrics.has_test_directory:

            findings.append(
                Finding(
                    id="STR005",
                    category="Structure",
                    severity="MEDIUM",
                    title="Test Directory Missing",
                    message="No dedicated test directory detected.",
                    recommendation="Add a tests/ directory for automated tests."
                )
            )




        if metrics.root_file_count > 20:

            findings.append(
                Finding(
                    id="STR008",
                    category="Structure",
                    severity="MEDIUM",
                    title="Too Many Root Files",
                    message=f"Repository contains {metrics.root_file_count} files in the project root.",
                    recommendation="Move related files into appropriate directories."
                )
            )

        if not metrics.has_gitignore:

            findings.append(
                Finding(
                    id="STR009",
                    category="Structure",
                    severity="HIGH",
                    title=".gitignore Missing",
                    message="Repository does not contain a .gitignore file.",
                    recommendation="Add a .gitignore file to avoid committing unnecessary files."
                )
            )

        if not metrics.has_editorconfig:

            findings.append(
                Finding(
                    id="STR010",
                    category="Structure",
                    severity="LOW",
                    title=".editorconfig Missing",
                    message="Repository does not contain an .editorconfig file.",
                    recommendation="Add an .editorconfig to enforce consistent formatting."
                )
            )

        return findings