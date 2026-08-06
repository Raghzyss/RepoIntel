"""
RepoIntel — Header Section
===========================
The top-of-page hero: wordmark, tagline, a GitHub repository URL input,
and a premium "Analyze" call-to-action.

This module assumes `styles.py` has already been imported and that
`inject_theme()` + `load_css()` have already been called elsewhere
(e.g. in app.py) so all `ri-*` classes and CSS variables are available.
No CSS is (re)injected here — only markup + minimal layout wiring.

Usage
-----
    import streamlit as st
    from styles import inject_theme, load_css
    from header_section import render_header

    st.set_page_config(page_title="RepoIntel", layout="wide")
    inject_theme()
    load_css()

    repo_url, analyze_clicked = render_header()

    if analyze_clicked and repo_url:
        ...
"""

import streamlit as st


def render_header(
    default_url: str = "",
    placeholder: str = "https://github.com/owner/repository",
):
    """
    Render the RepoIntel header: wordmark, tagline, repo URL input, and
    the Analyze button.

    Returns
    -------
    tuple[str, bool]
        (repo_url, analyze_clicked) — the current value of the URL input
        and whether the Analyze button was clicked on this run.
    """

    # --- Wordmark + tagline -------------------------------------------------
    st.markdown(
        """
        <div class="ri-header">
            <div class="ri-header__mark">
                <span class="ri-header__dot"></span>
                <span class="ri-header__wordmark">RepoIntel</span>
            </div>
            <div class="ri-header__tagline">
                Deterministic Repository Engineering Review Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- URL input + Analyze button -----------------------------------------
    st.markdown('<div class="ri-search">', unsafe_allow_html=True)

    input_col, button_col = st.columns([6, 1], gap="small")

    with input_col:
        repo_url = st.text_input(
            label="GitHub repository URL",
            value=default_url,
            placeholder=placeholder,
            label_visibility="collapsed",
            key="ri_repo_url_input",
        )

    with button_col:
        analyze_clicked = st.button(
            "Analyze",
            key="ri_analyze_button",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # --- Scoped styling for this section only --------------------------------
    # (Layout-critical rules specific to the header; the shared design
    # system itself lives entirely in styles.py.)
    st.markdown(
        """
        <style>
        .ri-header {
            text-align: center;
            padding: 3.5rem 0 2.25rem 0;
            animation: ri-fade-in var(--ri-base) var(--ri-ease);
        }

        .ri-header__mark {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.85rem;
        }

        .ri-header__dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: var(--ri-text-primary);
            display: inline-block;
        }

        .ri-header__wordmark {
            font-family: var(--ri-font-sans);
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            color: var(--ri-text-primary);
            line-height: 1;
        }

        .ri-header__tagline {
            font-family: var(--ri-font-sans);
            font-size: 1rem;
            font-weight: 450;
            letter-spacing: -0.005em;
            color: var(--ri-text-tertiary);
        }

        .ri-search {
            max-width: 720px;
            margin: 0 auto 3rem auto;
        }

        /* Repo URL input — elevate above the standard text input styling */
        .ri-search div[data-testid="stTextInput"] input {
            height: 3rem;
            font-size: 0.95rem;
            font-family: var(--ri-font-mono);
            padding-left: 1rem;
            border-radius: var(--ri-radius-md) !important;
            box-shadow: var(--ri-shadow-sm);
        }

        .ri-search div[data-testid="stTextInput"] input:focus {
            box-shadow: var(--ri-shadow-focus), var(--ri-shadow-sm);
        }

        .ri-search div[data-testid="stTextInput"] input::placeholder {
            color: var(--ri-text-tertiary);
            opacity: 0.8;
        }

        /* Analyze button — premium, full-height match with the input */
        .ri-search div[data-testid="column"]:nth-of-type(2) .stButton > button {
            height: 3rem;
            width: 100%;
            font-size: 0.95rem;
            font-weight: 600;
            border-radius: var(--ri-radius-md) !important;
            box-shadow: var(--ri-shadow-sm);
        }

        .ri-search div[data-testid="column"]:nth-of-type(2) .stButton > button:hover {
            box-shadow: var(--ri-shadow-md);
            transform: translateY(-1px);
        }

        @media (max-width: 640px) {
            .ri-header__wordmark { font-size: 2rem; }
            .ri-search { padding: 0 0.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    return repo_url, analyze_clicked
