"""
RepoIntel — Engineering Score Section
=======================================
The hero section of the report: a large overall Engineering Score with
its rating, followed by six domain scorecards (Documentation, Structure,
Code, Dependencies, Security, Project Health), each with its own
score and progress indicator.

This module assumes `styles.py` has already been imported and that
`inject_theme()` + `load_css()` have already been called elsewhere
(e.g. in app.py), so all `--ri-*` CSS variables and `ri-*` classes are
already available on the page. No stylesheet is (re)injected here —
only markup that consumes the existing design tokens inline.

Usage
-----
    import streamlit as st
    from styles import inject_theme, load_css
    from score_section import render_score_section

    st.set_page_config(page_title="RepoIntel", layout="wide")
    inject_theme()
    load_css()

    render_score_section()
"""

import streamlit as st
from core.scoring.overall_score import OverallScore

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _rating_variant(rating: str) -> str:
    """Map a rating label to a semantic tone using existing design tokens."""
    return {
        "Excellent": "success",
        "Good": "accent",
        "Fair": "warning",
        "Poor": "danger",
    }.get(rating, "neutral")


def _tone_colors(variant: str) -> tuple:
    """Return (fill color var, soft bg var) for a given semantic tone."""
    return {
        "success": ("var(--ri-success)", "var(--ri-success-soft)"),
        "accent": ("var(--ri-accent)", "var(--ri-accent-soft)"),
        "warning": ("var(--ri-warning)", "var(--ri-warning-soft)"),
        "danger": ("var(--ri-danger)", "var(--ri-danger-soft)"),
        "neutral": ("var(--ri-text-secondary)", "var(--ri-surface-hover)"),
    }.get(variant, ("var(--ri-accent)", "var(--ri-accent-soft)"))


def _progress_bar_html(score: int, max_score: int, variant: str = "accent") -> str:
    """
    Build a slim, rounded progress bar using the existing design tokens
    (CSS variables + radii + easing already defined in styles.py).
    No new stylesheet rules are declared — only inline styles referencing
    tokens that are already global on the page.
    """
    pct = 0 if max_score == 0 else max(0, min(100, round((score / max_score) * 100)))
    fill_color, _ = _tone_colors(variant)
    return f"""
    <div style="
        width:100%;
        height:8px;
        background-color:var(--ri-surface-hover);
        border-radius:var(--ri-radius-pill);
        overflow:hidden;
        margin-top:0.65rem;
    ">
        <div style="
            width:{pct}%;
            height:100%;
            background-color:{fill_color};
            border-radius:var(--ri-radius-pill);
            transition:width var(--ri-base) var(--ri-ease);
        "></div>
    </div>
    """


def _domain_card_html(name: str, icon: str, score: int, max_score: int) -> str:
    """Compose one domain scorecard as a single ri-card HTML block."""
    variant = _rating_variant(_score_to_rating(score, max_score))
    fill_color, _ = _tone_colors(variant)
    return f"""
    <div class="ri-card ri-card--hover" style="padding:22px 24px;">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:0.55rem;">
                <span style="font-size:1.1rem; line-height:1;">{icon}</span>
                <span style="
                    font-family:var(--ri-font-sans);
                    font-weight:600;
                    font-size:0.92rem;
                    color:var(--ri-text-primary);
                    letter-spacing:-0.01em;
                ">{name}</span>
            </div>
            <span style="
                font-family:var(--ri-font-mono);
                font-weight:600;
                font-size:0.9rem;
                color:{fill_color};
            ">{score}<span style="color:var(--ri-text-tertiary); font-weight:500;">/{max_score}</span></span>
        </div>
        {_progress_bar_html(score, max_score, variant)}
    </div>
    """


def _score_to_rating(score: int, max_score: int) -> str:
    """Derive a per-domain rating label from its score ratio."""
    if max_score == 0:
        return "Fair"
    ratio = score / max_score
    if ratio >= 0.85:
        return "Excellent"
    if ratio >= 0.70:
        return "Good"
    if ratio >= 0.50:
        return "Fair"
    return "Poor"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_score_section(score: OverallScore) -> None:
    overall_score = score.overall_score
    overall_max = 100

    if overall_score >= 85:
        overall_rating = "Excellent"
    elif overall_score >= 70:
        overall_rating = "Good"
    elif overall_score >= 50:
        overall_rating = "Fair"
    else:
        overall_rating = "Poor"

    domains = [
        {
            "name": "Documentation",
            "icon": "📄",
            "score": score.documentation.current_score,
            "max": score.documentation.max_score,
        },
        {
            "name": "Structure",
            "icon": "🏗️",
            "score": score.structure.current_score,
            "max": score.structure.max_score,
        },
        {
            "name": "Code",
            "icon": "🧩",
            "score": score.code.current_score,
            "max": score.code.max_score,
        },
        {
            "name": "Dependencies",
            "icon": "📦",
            "score": score.dependency.current_score,
            "max": score.dependency.max_score,
        },
        {
            "name": "Security",
            "icon": "🔒",
            "score": score.security.current_score,
            "max": score.security.max_score,
        },
        {
            "name": "Project Health",
            "icon": "💚",
            "score": score.health.current_score,
            "max": score.health.max_score,
        },
    ]

    variant = _rating_variant(overall_rating)
    fill_color, soft_bg = _tone_colors(variant)

    # --- Overall score hero --------------------------------------------------
    st.markdown(
        f"""
        <div style="text-align:center; padding: 1.5rem 0 3rem 0;">
            <div style="
                font-family:var(--ri-font-sans);
                font-weight:700;
                font-size:6rem;
                line-height:1;
                letter-spacing:-0.045em;
                color:var(--ri-text-primary);
            ">
                {overall_score}<span style="
                    font-size:2.25rem;
                    font-weight:600;
                    color:var(--ri-text-tertiary);
                    letter-spacing:-0.02em;
                ">/{overall_max}</span>
            </div>
            <div style="
                font-family:var(--ri-font-sans);
                font-size:0.85rem;
                font-weight:600;
                letter-spacing:0.06em;
                text-transform:uppercase;
                color:var(--ri-text-tertiary);
                margin:0.6rem 0 1.1rem 0;
            ">Engineering Score</div>
            <span style="
                display:inline-flex;
                align-items:center;
                padding:0.4rem 1rem;
                border-radius:var(--ri-radius-pill);
                background-color:{soft_bg};
                color:{fill_color};
                font-family:var(--ri-font-sans);
                font-weight:650;
                font-size:0.9rem;
                letter-spacing:-0.005em;
            ">{overall_rating}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Domain scorecards grid ----------------------------------------------
    row1 = st.columns(3, gap="medium")
    row2 = st.columns(3, gap="medium")

    for col, domain in zip(row1 + row2, domains[:6]):
        with col:
            st.markdown(
                _domain_card_html(
                    name=domain.get("name", ""),
                    icon=domain.get("icon", "•"),
                    score=domain.get("score", 0),
                    max_score=domain.get("max", 20),
                ),
                unsafe_allow_html=True,
            )
