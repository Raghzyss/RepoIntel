"""
RepoIntel — Repository Overview Section
=========================================
A premium summary of the analyzed repository: identity (name + owner),
core statistics as metric cards, a language composition bar with
elegant rounded pills, and a technology stack badge row.

This module assumes `styles.py` has already been imported and that
`inject_theme()` + `load_css()` have already been called elsewhere
(e.g. in app.py), so all `--ri-*` CSS variables, `ri-*` classes, and
the `card` / `badge` / `metric_card` / `section_title` helpers are
already available. No stylesheet is (re)injected here — only markup
that consumes the existing design tokens (inline styles + helpers
from styles.py).

Usage
-----
    import streamlit as st
    from styles import inject_theme, load_css
    from repository_section import render_repository_section

    st.set_page_config(page_title="RepoIntel", layout="wide")
    inject_theme()
    load_css()

    render_repository_section()
"""

import streamlit as st
from models.repository import Repository
from ui.styles import card, metric_card, section_title


# ---------------------------------------------------------------------------
# Placeholder data — swap these out for real analysis results upstream.
# ---------------------------------------------------------------------------

# Familiar, muted per-language accent colors (GitHub-linguist inspired).
# Used only as small identity dots / bar segments — never as large fills.
LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#F1E05A",
    "TypeScript": "#3178C6",
    "Java": "#B07219",
    "Go": "#00ADD8",
    "Rust": "#DEA584",
    "C++": "#F34B7D",
    "C": "#555555",
    "C#": "#178600",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "HTML": "#E34C26",
    "CSS": "#563D7C",
    "SCSS": "#C6538C",
    "Shell": "#89E051",
    "Dockerfile": "#384D54",
    "Vue": "#41B883",
}
_LANGUAGE_COLOR_FALLBACK = "#8A8A92"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _language_color(name: str) -> str:
    """Resolve a stable accent color for a language, with a neutral fallback."""
    return LANGUAGE_COLORS.get(name, _LANGUAGE_COLOR_FALLBACK)


def _format_int(value: int) -> str:
    """Thousands-separated integer for display (e.g. 48213 -> '48,213')."""
    return f"{value:,}"


def _language_bar_html(languages: list) -> str:
    """
    A slim horizontal composition bar — one segment per language, width
    proportional to its share. A quiet, GitHub-style summary strip that
    sits above the individual language pills.
    """
    segments = "".join(
        f'<div style="'
        f"width:{lang.get('percentage', 0)}%;"
        f"height:100%;"
        f"background-color:{_language_color(lang.get('name', ''))};"
        f'"></div>'
        for lang in languages
    )
    return f"""
    <div style="
        width:100%;
        height:10px;
        border-radius:var(--ri-radius-pill);
        overflow:hidden;
        display:flex;
        background-color:var(--ri-surface-hover);
        margin-bottom:1.1rem;
    ">
        {segments}
    </div>
    """


def _language_pill_html(name: str, percentage: float) -> str:
    """An elegant rounded pill: color dot + language name + percentage."""
    color = _language_color(name)
    return f"""
    <span style="
        display:inline-flex;
        align-items:center;
        gap:0.45rem;
        padding:0.35rem 0.8rem 0.35rem 0.6rem;
        border-radius:var(--ri-radius-pill);
        background-color:var(--ri-surface-hover);
        border:1px solid var(--ri-border);
        font-family:var(--ri-font-sans);
        font-size:0.82rem;
        font-weight:600;
        color:var(--ri-text-secondary);
        letter-spacing:-0.005em;
        margin:0 0.5rem 0.5rem 0;
    ">
        <span style="
            width:8px;
            height:8px;
            border-radius:50%;
            background-color:{color};
            flex-shrink:0;
        "></span>
        {name}
        <span style="color:var(--ri-text-tertiary); font-weight:500;">
            {percentage:g}%
        </span>
    </span>
    """


def _tech_badge_html(name: str) -> str:
    """
    A technology stack badge — visually distinct from language pills
    (square-ish corners, monospace label) to read as "stack" rather
    than "language composition".
    """
    return f"""
    <span style="
        display:inline-flex;
        align-items:center;
        padding:0.38rem 0.75rem;
        border-radius:var(--ri-radius-sm);
        background-color:var(--ri-bg);
        border:1px solid var(--ri-border-strong);
        font-family:var(--ri-font-mono);
        font-size:0.78rem;
        font-weight:600;
        color:var(--ri-text-primary);
        letter-spacing:-0.005em;
        margin:0 0.5rem 0.5rem 0;
        box-shadow:var(--ri-shadow-xs);
    ">
        {name}
    </span>
    """


def _identity_card_html(repo_name: str, owner: str) -> str:
    """Repository identity block: avatar initial, name, and owner path."""
    initial = (repo_name[:1] or "?").upper()
    return f"""
    <div style="display:flex; align-items:center; gap:1rem;">
        <div style="
            width:52px;
            height:52px;
            border-radius:var(--ri-radius-md);
            background-color:var(--ri-text-primary);
            color:var(--ri-text-inverse);
            display:flex;
            align-items:center;
            justify-content:center;
            font-family:var(--ri-font-sans);
            font-size:1.3rem;
            font-weight:700;
            flex-shrink:0;
        ">{initial}</div>
        <div>
            <div style="
                font-family:var(--ri-font-sans);
                font-size:1.35rem;
                font-weight:700;
                letter-spacing:-0.02em;
                color:var(--ri-text-primary);
                line-height:1.25;
            ">{repo_name}</div>
            <div style="
                font-family:var(--ri-font-mono);
                font-size:0.85rem;
                color:var(--ri-text-tertiary);
            ">{owner}/{repo_name}</div>
        </div>
    </div>
    """


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_repository_section(repository: Repository) -> None:
    """
    Render the full Repository Overview section: identity card, a
    four-up row of statistic metric cards, a language composition
    bar with rounded pills, and a technology stack badge row.

    Parameters
    ----------
    repo_name, owner : str
        The repository name and owning user/organization.
    total_files, total_lines : int
        Aggregate repository statistics.
    languages : list[dict], optional
        Each dict: {"name": str, "percentage": float}. Should sum to
        ~100. Defaults to RepoIntel's placeholder language mix.
    tech_stack : list[str], optional
        Detected frameworks / tools / infra. Defaults to a placeholder
        stack.
    """
    repo_name = repository.name
    owner = repository.owner
    total_files = repository.total_files
    total_lines = repository.total_lines

    total = sum(repository.languages.values()) or 1
    languages = [
        {
            "name": name,
            "percentage": round((count / total) * 100, 1),
        }
        for name, count in sorted(
            repository.languages.items(),
            key=lambda x: x[1],
            reverse=True,
        )
    ]

    tech_stack = []
    for values in repository.technology_stack.values():
        tech_stack.extend(values)
    tech_stack = sorted(set(tech_stack))

    st.markdown(
        section_title(
            "Repository Overview",
            "Identity, footprint, and detected technology stack",
        ),
        unsafe_allow_html=True,
    )

    # --- Identity card --------------------------------------------------
    st.markdown(
        card(_identity_card_html(repo_name, owner), padding="24px 26px"),
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)

    # --- Statistics grid --------------------------------------------------
    stat_cols = st.columns(4, gap="medium")
    stats = [
        ("Total Files", _format_int(total_files)),
        ("Total Lines", _format_int(total_lines)),
        ("Languages", str(len(languages))),
        ("Tech Stack", str(len(tech_stack))),
    ]
    for col, (label, value) in zip(stat_cols, stats):
        with col:
            st.markdown(metric_card(label, value), unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # --- Languages card --------------------------------------------------
    language_bar = _language_bar_html(languages)
    language_pills = "".join(
        _language_pill_html(lang["name"], lang["percentage"])
        for lang in languages
    )
    st.markdown(
        card(
            (
                '<div style="'
                'font-family:var(--ri-font-sans);'
                'font-size:0.78rem;'
                'font-weight:600;'
                'text-transform:uppercase;'
                'letter-spacing:0.045em;'
                'color:var(--ri-text-tertiary);'
                'margin-bottom:0.9rem;'
                '">Languages</div>'
                + language_bar
                + language_pills
            ),
            padding="22px 24px",
            hover=False,
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)

    # --- Technology stack card --------------------------------------------
    tech_body = "".join(_tech_badge_html(tech) for tech in tech_stack)
    st.markdown(
            card(
            (
                '<div style="'
                'font-family:var(--ri-font-sans);'
                'font-size:0.78rem;'
                'font-weight:600;'
                'text-transform:uppercase;'
                'letter-spacing:0.045em;'
                'color:var(--ri-text-tertiary);'
                'margin-bottom:0.9rem;'
                '">Technology Stack</div>'
                '<div>'
                + tech_body +
                '</div>'
            ),
            padding="22px 24px",
            hover=False,
        ),
        unsafe_allow_html=True,
    )
