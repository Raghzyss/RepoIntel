import streamlit as st


def display_structure_section(analysis):

    structure = analysis["structure"]

    st.subheader("Structure Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Total Directories:** {structure['total_directories']}")
        st.write(f"**Maximum Depth:** {structure['max_depth']}")
        st.write(f"**Empty Directories:** {structure['empty_directories']}")

    with col2:
        st.write(f"**Large Files:** {len(structure['large_files'])}")
        st.write(
            f"**Well Structured:** {'✅' if structure['well_structured'] else '❌'}"
        )

    if structure["large_files"]:
        st.subheader("Large Files")
        st.write(structure["large_files"])