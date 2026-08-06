"""
RepoIntel — AI Engineering Advisor Section
=============================================
A premium "coming soon" placeholder for the future AI Advisor feature:
personalized engineering recommendations synthesized from a repo's
findings, classification, and engineering score.

This module assumes `styles.py` has already been imported and that
`inject_theme()` + `load_css()` have already been called elsewhere
(e.g. in app.py), so all `--ri-*` CSS variables, `ri-*` classes, and
the `card` / `badge` / `section_title` helpers are already available.
No stylesheet is (re)injected here — only markup that consumes the
existing design tokens (inline styles + helpers from styles.py).

Usage
-----
    import streamlit as st
    from styles import inject_theme, load_css
    from advisor_section import render_advisor_section

    st.set_page_config(page_title="RepoIntel", layout="wide")
    inject_theme()
    load_css()

    render_advisor_section()
"""

import streamlit as st

from styles import card, badge, section_title


def render_advisor_section() -> None:
    """
    Render the AI Engineering Advisor placeholder: a quiet, premium
    "feature coming soon" card with a title, subtitle badge, body copy,
    and a beautifully disabled call-to-action button.
    """
    st.markdown(
        section_title(
            "🤖 AI Engineering Advisor",
            "Personalized recommendations, synthesized from your review",
        ),
        unsafe_allow_html=True,
    )

    body = f"""
    <div style="text-align:center; padding:2.75rem 1.5rem 2.5rem 1.5rem;">
        <div style="
            width:64px;
            height:64px;
            margin:0 auto 1.4rem auto;
            border-radius:var(--ri-radius-md);
            background-color:var(--ri-accent-soft);
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:1.6rem;
            line-height:1;
        ">🤖</div>

        {badge("Coming Soon", "accent")}

        <div style="
            font-family:var(--ri-font-sans);
            font-size:1.3rem;
            font-weight:700;
            letter-spacing:-0.02em;
            color:var(--ri-text-primary);
            margin:1rem auto 0.75rem auto;
            max-width:520px;
            line-height:1.3;
        ">AI-generated recommendations, tailored to this repository</div>

        <div style="
            font-family:var(--ri-font-sans);
            font-size:0.93rem;
            font-weight:450;
            line-height:1.7;
            color:var(--ri-text-secondary);
            max-width:480px;
            margin:0 auto 1.9rem auto;
            letter-spacing:-0.003em;
        ">RepoIntel will soon generate personalized engineering
        recommendations based on repository findings, project
        classification and engineering score.</div>

        <button disabled style="
            font-family:var(--ri-font-sans);
            font-size:0.9rem;
            font-weight:600;
            letter-spacing:-0.005em;
            color:var(--ri-text-tertiary);
            background-color:var(--ri-surface-hover);
            border:1px solid var(--ri-border-strong);
            border-radius:var(--ri-radius-md);
            padding:0.72rem 1.6rem;
            cursor:not-allowed;
            box-shadow:var(--ri-shadow-xs);
        ">Generate Recommendations</button>
    </div>
    """

    st.markdown(
        card(body, padding="8px", hover=False),
        unsafe_allow_html=True,
    )
