import streamlit as st

from core.collector.collector import RepositoryCollector

st.set_page_config(
    page_title="RepoIntel",
    page_icon="📦",
    layout="wide"
)

st.title("📦 RepoIntel")
st.subheader("AI-Powered Repository Intelligence Platform")

url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)

if st.button("Collect Repository"):

    if not url:
        st.warning("Please enter a GitHub repository URL.")
        st.stop()

    try:
        collector = RepositoryCollector()
        repository = collector.collect(url)

        st.success("Repository collected successfully!")

        st.subheader("Repository Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Repository:** {repository.name}")
            st.write(f"**Owner:** {repository.owner}")
            st.write(f"**Total Lines:** {repository.total_lines}")

        with col2:
            st.write(f"**Total Files:** {repository.total_files}")
            st.write(f"**Source Files:** {len(repository.source_files)}")

        st.subheader("Detected Languages")
        st.json(repository.languages)

        st.subheader("Technology Stack")

        if repository.technology_stack:

            for category, technologies in repository.technology_stack.items():

                st.markdown(f"### {category}")

                for technology in technologies:
                    st.success(technology)

        else:
            st.info("No technologies detected.")

        st.subheader("Configuration Files")
        st.write(list(repository.config_files.keys()))

        if repository.readme:
            st.subheader("README Preview")
            st.code(repository.readme[:1000], language="markdown")

        st.subheader("Folder Structure (First 20 Entries)")
        st.write(repository.folder_tree[:20])

    except Exception as e:
        st.error(f"Error: {e}")