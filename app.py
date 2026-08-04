import streamlit as st

from core.collector.collector import RepositoryCollector

from core.extractor.documentation_extractor import DocumentationExtractor
from core.extractor.structure_extractor import StructureExtractor
from core.extractor.code_extractor import CodeExtractor
from core.extractor.dependency_extractor import DependencyExtractor
from core.extractor.security_extractor import SecurityExtractor
from core.extractor.project_health_extractor import ProjectHealthExtractor

from core.rules.rule_engine import RuleEngine


st.set_page_config(
    page_title="RepoIntel",
    page_icon="📦",
    layout="wide",
)

st.title("📦 RepoIntel")
st.subheader("Deterministic Repository Engineering Review Platform")

url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
)

if st.button("Analyze Repository"):

    if not url:
        st.warning("Please enter a GitHub repository URL.")
        st.stop()

    try:

        with st.spinner("Collecting repository..."):

            repository = RepositoryCollector().collect(url)

        with st.spinner("Running extractors..."):

            repository = DocumentationExtractor().extract(repository)
            repository = StructureExtractor().extract(repository)
            repository = CodeExtractor().extract(repository)
            repository = DependencyExtractor().extract(repository)
            repository = SecurityExtractor().extract(repository)
            repository = ProjectHealthExtractor().extract(repository)

        with st.spinner("Running rule engine..."):

            findings = RuleEngine().evaluate(repository)

        st.success("Repository analyzed successfully!")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Repository")

            st.write("**Name:**", repository.name)
            st.write("**Owner:**", repository.owner)
            st.write("**Total Files:**", repository.total_files)
            st.write("**Total Lines:**", repository.total_lines)

        with col2:

            st.subheader("Languages")

            if repository.languages:
                st.json(repository.languages)
            else:
                st.info("No languages detected.")

        st.subheader("Technology Stack")

        if repository.technology_stack:
            st.json(repository.technology_stack)
        else:
            st.info("No technologies detected.")

        st.divider()

        st.subheader(f"Engineering Findings ({len(findings)})")

        if not findings:
            st.success("🎉 No findings detected.")

        for finding in findings:

            with st.expander(
                f"[{finding.severity}] {finding.id} - {finding.title}"
            ):

                st.write(f"**Category:** {finding.category}")
                st.write(f"**Message:** {finding.message}")
                st.write(f"**Recommendation:** {finding.recommendation}")
                st.subheader("Config Files")
                st.json(
                    {
                        name: str(path)
                        for name, path in repository.config_files.items()
                    }
                )

    except Exception as e:

        st.exception(e)