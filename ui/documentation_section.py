import streamlit as st


def display_documentation_section(analysis):

    documentation = analysis["documentation"]

    st.subheader("Documentation Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**README Present:** {'✅' if documentation['readme_present'] else '❌'}"
        )

        st.write(
            f"**README Length:** {documentation['readme_length']} characters"
        )

        st.write(
            f"**Installation Guide:** {'✅' if documentation['installation'] else '❌'}"
        )

    with col2:

        st.write(
            f"**Usage Section:** {'✅' if documentation['usage'] else '❌'}"
        )

        st.write(
            f"**License Section:** {'✅' if documentation['license'] else '❌'}"
        )

        st.write(
            f"**Contributing Section:** {'✅' if documentation['contributing'] else '❌'}"
        )

    st.metric(
        "Documentation Score",
        f"{documentation['score']}/100",
    )