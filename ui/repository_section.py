import streamlit as st


def display_repository_section(repository):

    st.subheader("Repository Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Repository:** {repository.name}")
        st.write(f"**Owner:** {repository.owner}")
        st.write(f"**Total Lines:** {repository.total_lines}")

    with col2:
        st.write(f"**Total Files:** {repository.total_files}")
        st.write(f"**Source Files:** {len(repository.source_files)}")

    st.subheader("Configuration Files")
    st.write(list(repository.config_files.keys()))

    if repository.readme:
        st.subheader("README Preview")
        st.code(repository.readme[:1000], language="markdown")

    st.subheader("Folder Structure (First 20 Entries)")
    st.write(repository.folder_tree[:20])