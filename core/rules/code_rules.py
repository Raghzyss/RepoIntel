from models.code_metrics import CodeMetrics
from models.finding import Finding


class CodeRules:
    """
    Evaluates source code metrics and produces engineering findings.
    """

    def evaluate(
        self,
        metrics: CodeMetrics,
    ) -> list[Finding]:

        findings: list[Finding] = []

        if metrics.total_source_files == 0:

            findings.append(
                Finding(
                    id="CODE001",
                    category="Code Engineering",
                    severity="HIGH",
                    title="No Source Files",
                    message="Repository does not contain any source files.",
                    recommendation="Add source code to the repository."
                )
            )

            return findings

        if metrics.files_over_1000_lines > 0:

            findings.append(
                Finding(
                    id="CODE002",
                    category="Code Engineering",
                    severity="HIGH",
                    title="Very Large Source Files",
                    message=f"{metrics.files_over_1000_lines} source files exceed 1000 lines.",
                    recommendation="Split very large files into smaller modules."
                )
            )

        elif metrics.files_over_500_lines > 3:

            findings.append(
                Finding(
                    id="CODE003",
                    category="Code Engineering",
                    severity="MEDIUM",
                    title="Large Source Files",
                    message=f"{metrics.files_over_500_lines} files exceed 500 lines.",
                    recommendation="Consider modularizing large files."
                )
            )

        if metrics.comment_line_percentage < 5:

            findings.append(
                Finding(
                    id="CODE004",
                    category="Code Engineering",
                    severity="LOW",
                    title="Low Comment Coverage",
                    message=f"Only {metrics.comment_line_percentage:.1f}% of lines are comments.",
                    recommendation="Add meaningful comments where appropriate."
                )
            )

        if metrics.todo_count > 20:

            findings.append(
                Finding(
                    id="CODE005",
                    category="Code Engineering",
                    severity="HIGH",
                    title="Large Number of TODOs",
                    message=f"{metrics.todo_count} TODO comments detected.",
                    recommendation="Resolve pending TODO items."
                )
            )

        elif metrics.todo_count > 5:

            findings.append(
                Finding(
                    id="CODE006",
                    category="Code Engineering",
                    severity="MEDIUM",
                    title="TODO Comments Present",
                    message=f"{metrics.todo_count} TODO comments detected.",
                    recommendation="Review outstanding TODO comments."
                )
            )

        if metrics.fixme_count > 0:

            findings.append(
                Finding(
                    id="CODE007",
                    category="Code Engineering",
                    severity="MEDIUM",
                    title="FIXME Comments Present",
                    message=f"{metrics.fixme_count} FIXME comments detected.",
                    recommendation="Resolve FIXME issues."
                )
            )

        if metrics.hack_count > 0:

            findings.append(
                Finding(
                    id="CODE008",
                    category="Code Engineering",
                    severity="MEDIUM",
                    title="Hack Comments Present",
                    message=f"{metrics.hack_count} HACK comments detected.",
                    recommendation="Replace temporary hacks with maintainable implementations."
                )
            )

        if metrics.xxx_count > 0:

            findings.append(
                Finding(
                    id="CODE009",
                    category="Code Engineering",
                    severity="LOW",
                    title="XXX Comments Present",
                    message=f"{metrics.xxx_count} XXX comments detected.",
                    recommendation="Review XXX markers."
                )
            )

        if metrics.generated_files > 0:

            findings.append(
                Finding(
                    id="CODE010",
                    category="Code Engineering",
                    severity="LOW",
                    title="Generated Files Present",
                    message=f"{metrics.generated_files} generated files detected.",
                    recommendation="Exclude generated files from engineering evaluation where appropriate."
                )
            )

        if metrics.minified_files > 0:

            findings.append(
                Finding(
                    id="CODE011",
                    category="Code Engineering",
                    severity="LOW",
                    title="Minified Files Present",
                    message=f"{metrics.minified_files} minified files detected.",
                    recommendation="Exclude minified files from repository source where possible."
                )
            )

        if metrics.duplicate_file_names > 0:

            findings.append(
                Finding(
                    id="CODE012",
                    category="Code Engineering",
                    severity="LOW",
                    title="Duplicate File Names",
                    message=f"{metrics.duplicate_file_names} duplicate file names detected.",
                    recommendation="Rename duplicate files to improve clarity."
                )
            )

        python_files = metrics.source_file_extensions.get(
            ".py",
            0,
        )

        if (
            metrics.total_source_files > 0
            and python_files / metrics.total_source_files >= 0.6
            and metrics.total_functions > 20
            and metrics.docstring_count == 0
        ):

            findings.append(
                Finding(
                    id="CODE013",
                    category="Code Engineering",
                    severity="LOW",
                    title="No Docstrings",
                    message="No docstrings were detected despite multiple functions.",
                    recommendation="Document public functions using docstrings."
                )
            )

        return findings