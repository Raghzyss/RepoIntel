from models.finding import Finding
from models.security_metrics import SecurityMetrics


class SecurityRules:
    """
    Evaluates security metrics and produces engineering findings.
    """

    def evaluate(
        self,
        metrics: SecurityMetrics,
    ) -> list[Finding]:

        findings: list[Finding] = []

        if metrics.potential_secrets > 0:

            findings.append(
                Finding(
                    id="SEC001",
                    category="Security",
                    severity="HIGH",
                    title="Potential Secrets Detected",
                    message=f"{metrics.potential_secrets} potential secrets were detected.",
                    recommendation="Remove secrets and use environment variables or secret managers."
                )
            )

        if metrics.private_keys > 0:

            findings.append(
                Finding(
                    id="SEC002",
                    category="Security",
                    severity="CRITICAL",
                    title="Private Keys Detected",
                    message=f"{metrics.private_keys} private key(s) detected.",
                    recommendation="Immediately remove private keys from the repository."
                )
            )

        if metrics.aws_keys > 0:

            findings.append(
                Finding(
                    id="SEC003",
                    category="Security",
                    severity="CRITICAL",
                    title="AWS Credentials Detected",
                    message=f"{metrics.aws_keys} AWS access key(s) detected.",
                    recommendation="Rotate compromised credentials immediately."
                )
            )

        if metrics.github_tokens > 0:

            findings.append(
                Finding(
                    id="SEC004",
                    category="Security",
                    severity="CRITICAL",
                    title="GitHub Tokens Detected",
                    message=f"{metrics.github_tokens} GitHub token(s) detected.",
                    recommendation="Revoke exposed GitHub tokens immediately."
                )
            )

        if metrics.google_api_keys > 0:

            findings.append(
                Finding(
                    id="SEC005",
                    category="Security",
                    severity="HIGH",
                    title="Google API Keys Detected",
                    message=f"{metrics.google_api_keys} Google API key(s) detected.",
                    recommendation="Move API keys to environment variables."
                )
            )

        if metrics.has_env_file:

            findings.append(
                Finding(
                    id="SEC006",
                    category="Security",
                    severity="MEDIUM",
                    title=".env File Present",
                    message="A .env file exists inside the repository.",
                    recommendation="Avoid committing .env files."
                )
            )

        if (
            metrics.has_env_file
            and not metrics.has_env_example
        ):

            findings.append(
                Finding(
                    id="SEC007",
                    category="Security",
                    severity="LOW",
                    title=".env.example Missing",
                    message="No .env.example file detected.",
                    recommendation="Provide an example environment file."
                )
            )

        if metrics.eval_usage > 0:

            findings.append(
                Finding(
                    id="SEC008",
                    category="Security",
                    severity="HIGH",
                    title="eval() Usage Detected",
                    message=f"{metrics.eval_usage} eval() usages detected.",
                    recommendation="Avoid eval() where possible."
                )
            )

        if metrics.exec_usage > 0:

            findings.append(
                Finding(
                    id="SEC009",
                    category="Security",
                    severity="HIGH",
                    title="exec() Usage Detected",
                    message=f"{metrics.exec_usage} exec() usages detected.",
                    recommendation="Avoid exec() where possible."
                )
            )

        if metrics.shell_execution_usage > 0:

            findings.append(
                Finding(
                    id="SEC010",
                    category="Security",
                    severity="MEDIUM",
                    title="Shell Execution Detected",
                    message=f"{metrics.shell_execution_usage} shell execution calls detected.",
                    recommendation="Validate all user input before executing shell commands."
                )
            )

        return findings