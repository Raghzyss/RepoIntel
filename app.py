import streamlit as st

from ui.styles import inject_theme, load_css
from ui.header_section import render_header
from ui.score_section import render_score_section
from ui.repository_section import render_repository_section
from ui.classification_section import render_classification_section
from ui.findings_section import render_findings_section
from ui.advisor_section import render_advisor_section

from core.collector.collector import RepositoryCollector

from core.extractor.documentation_extractor import DocumentationExtractor
from core.extractor.structure_extractor import StructureExtractor
from core.extractor.code_extractor import CodeExtractor
from core.extractor.dependency_extractor import DependencyExtractor
from core.extractor.security_extractor import SecurityExtractor
from core.extractor.project_health_extractor import ProjectHealthExtractor

from core.rules.rule_engine import RuleEngine

from core.llm.project_classifier import ProjectClassifier
from core.scoring.scorer import Scorer


st.set_page_config(
    page_title="RepoIntel",
    page_icon="📦",
    layout="wide",
)


def run_pipeline(repo_url: str):
    """
    Executes the complete RepoIntel backend pipeline and returns
    the objects required by the UI.
    """

    with st.spinner("Collecting repository..."):
        repository = RepositoryCollector().collect(repo_url)

    with st.spinner("Running extractors..."):
        repository = DocumentationExtractor().extract(repository)
        repository = StructureExtractor().extract(repository)
        repository = CodeExtractor().extract(repository)
        repository = DependencyExtractor().extract(repository)
        repository = SecurityExtractor().extract(repository)
        repository = ProjectHealthExtractor().extract(repository)

    with st.spinner("Running rule engine..."):
        findings = RuleEngine().evaluate(repository)

    with st.spinner("Classifying repository..."):
        classification = ProjectClassifier().classify(repository)

    with st.spinner("Calculating engineering score..."):
        score = Scorer().score(
            findings=findings,
            classification=classification,
        )

    return repository, findings, classification, score


def main():

    inject_theme()
    load_css()

    repo_url, analyze_clicked = render_header()

    if not analyze_clicked:
        return

    if not repo_url:
        st.warning("Please enter a GitHub repository URL.")
        return

    try:

        repository, findings, classification, score = run_pipeline(repo_url)

        render_score_section(score)

        render_repository_section(repository)

        render_classification_section(classification)

        render_findings_section(findings)

        render_advisor_section()

    except Exception as e:
        st.exception(e)


if __name__ == "__main__":
    main()