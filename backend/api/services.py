"""Reusable orchestration for the RepoIntel analysis pipeline."""

from core.collector.collector import RepositoryCollector
from core.extractor.code_extractor import CodeExtractor
from core.extractor.dependency_extractor import DependencyExtractor
from core.extractor.documentation_extractor import DocumentationExtractor
from core.extractor.project_health_extractor import ProjectHealthExtractor
from core.extractor.security_extractor import SecurityExtractor
from core.extractor.structure_extractor import StructureExtractor
from core.llm.project_classifier import ProjectClassifier
from core.llm.schemas import ProjectClassification
from core.rules.rule_engine import RuleEngine
from core.scoring.overall_score import OverallScore
from core.scoring.scorer import Scorer
from models.finding import Finding
from models.repository import Repository


def run_pipeline(
    repo_url: str,
) -> tuple[
    Repository,
    list[Finding],
    ProjectClassification,
    OverallScore,
]:
    """Execute the complete existing RepoIntel backend pipeline."""

    repository = RepositoryCollector().collect(repo_url)

    repository = DocumentationExtractor().extract(repository)
    repository = StructureExtractor().extract(repository)
    repository = CodeExtractor().extract(repository)
    repository = DependencyExtractor().extract(repository)
    repository = SecurityExtractor().extract(repository)
    repository = ProjectHealthExtractor().extract(repository)

    findings = RuleEngine().evaluate(repository)

    classification = ProjectClassifier().classify(repository)

    score = Scorer().score(
        findings=findings,
        classification=classification,
    )

    return repository, findings, classification, score
