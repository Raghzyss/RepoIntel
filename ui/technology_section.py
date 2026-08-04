import streamlit as st


def display_technology_section(repository):

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