"""
RepoIntel — Engineering Findings Section
===========================================
The core diagnostic output of a RepoIntel review: individual engineering
findings — grouped by severity — each rendered as a self-contained issue
card (never an expander, never a table, never a plain markdown list).

Each finding card surfaces:
    Top     — severity badge, finding ID, title
    Middle  — the finding's message / description
    Bottom  — a visually separated recommendation container

This module assumes `styles.py` has already been imported and that
`inject_theme()` + `load_css()` have already been called elsewhere
(e.g. in app.py), so all `--ri-*` CSS variables, `ri-*` classes, and the
`card` / `badge` / `section_title` / `code_pill` helpers are already
available. No stylesheet is (re)injected here — only markup that
consumes the existing design tokens (inline styles + helpers from
styles.py), matching header_section.py / repository_section.py /
score_section.py / classification_section.py exactly.

Usage
-----
    import streamlit as st
from models.finding import Finding
    from ui.styles import inject_theme, load_css
    from findings_section import render_findings_section

    st.set_page_config(page_title="RepoIntel", layout="wide")
    inject_theme()
    load_css()

    render_findings_section()
"""

import streamlit as st
from models.finding import Finding

from ui.styles import card, badge, section_title, code_pill



# Ordered so the most severe findings render first, and so each group's
# heading follows a fixed, predictable sequence.
_SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]

_SEVERITY_META = {
    "Critical": {"emoji": "🔴", "badge_variant": "danger", "accent": "var(--ri-danger)"},
    "High": {"emoji": "🟠", "badge_variant": "warning", "accent": "var(--ri-warning)"},
    "Medium": {"emoji": "🟡", "badge_variant": "accent", "accent": "var(--ri-accent)"},
    "Low": {"emoji": "🟢", "badge_variant": "neutral", "accent": "var(--ri-text-tertiary)"},
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _severity_meta(severity: str) -> dict:
    """Resolve display metadata for a severity, with a quiet fallback."""
    return _SEVERITY_META.get(
        severity, {"emoji": "⚪", "badge_variant": "neutral", "accent": "var(--ri-text-tertiary)"}
    )


def _group_heading_html(severity: str, count: int) -> str:
    """A small, quiet section heading for one severity group."""
    meta = _severity_meta(severity)
    return f"""
    <div style="
        display:flex;
        align-items:center;
        gap:0.55rem;
        margin:0 0 0.85rem 0;
    ">
        <span style="font-size:0.95rem; line-height:1;">{meta['emoji']}</span>
        <span style="
            font-family:var(--ri-font-sans);
            font-size:1.02rem;
            font-weight:650;
            letter-spacing:-0.01em;
            color:var(--ri-text-primary);
        ">{severity}</span>
        <span style="
            font-family:var(--ri-font-mono);
            font-size:0.78rem;
            font-weight:600;
            color:var(--ri-text-tertiary);
            background-color:var(--ri-surface-hover);
            border:1px solid var(--ri-border);
            border-radius:var(--ri-radius-pill);
            padding:0.08rem 0.55rem;
        ">{count}</span>
    </div>
    """


def _recommendation_block_html(recommendation: str) -> str:
    """
    A visually separated container for the recommendation — a slightly
    raised, distinctly bordered panel so it reads as "the actionable
    takeaway" rather than another paragraph of body text.
    """
    return f"""
    <div style="
        background-color:var(--ri-bg);
        border:1px solid var(--ri-border-strong);
        border-radius:var(--ri-radius-sm);
        padding:14px 16px;
        margin-top:1rem;
        box-shadow:var(--ri-shadow-xs);
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:0.4rem;
            margin-bottom:0.35rem;
        ">
            <span style="color:var(--ri-accent); font-size:0.8rem; line-height:1;">&#8594;</span>
            <span style="
                font-family:var(--ri-font-sans);
                font-size:0.72rem;
                font-weight:650;
                text-transform:uppercase;
                letter-spacing:0.055em;
                color:var(--ri-text-tertiary);
            ">Recommendation</span>
        </div>
        <div style="
            font-family:var(--ri-font-sans);
            font-size:0.88rem;
            font-weight:450;
            line-height:1.6;
            color:var(--ri-text-secondary);
            letter-spacing:-0.005em;
        ">{recommendation}</div>
    </div>
    """


def _finding_card_html(finding: dict) -> str:
    """
    Compose a single finding as a premium issue card:
    severity badge + ID + title on top, message in the middle, and a
    visually distinct recommendation panel at the bottom. A thin,
    severity-tinted left edge gives quiet at-a-glance triage without
    resorting to bright colors.
    """
    severity = finding.get("severity", "Low")
    meta = _severity_meta(severity)

    top_row = f"""
    <div style="
        display:flex;
        align-items:center;
        gap:0.65rem;
        flex-wrap:wrap;
        margin-bottom:0.65rem;
    ">
        {badge(severity, meta['badge_variant'])}
        {code_pill(finding.get('id', ''))}
    </div>
    <div style="
        font-family:var(--ri-font-sans);
        font-size:1rem;
        font-weight:650;
        letter-spacing:-0.01em;
        color:var(--ri-text-primary);
        line-height:1.35;
        margin-bottom:0.6rem;
    ">{finding.get('title', '')}</div>
    """

    message_html = f"""
    <div style="
        font-family:var(--ri-font-sans);
        font-size:0.9rem;
        font-weight:450;
        line-height:1.65;
        color:var(--ri-text-secondary);
        letter-spacing:-0.003em;
    ">{finding.get('message', '')}</div>
    """

    body = top_row + message_html + _recommendation_block_html(finding.get("recommendation", ""))

    return f"""
    <div class="ri-card ri-card--hover" style="
        padding:22px 24px;
        border-left:3px solid {meta['accent']};
        margin-bottom:1rem;
    ">
        {body}
    </div>
    """


def _empty_group_html(severity: str) -> str:
    """A quiet placeholder shown when a severity group has no findings
    (only rendered when show_empty_groups=True)."""
    return f"""
    <div class="ri-card" style="
        padding:16px 20px;
        margin-bottom:1rem;
        box-shadow:none;
    ">
        <div style="
            font-family:var(--ri-font-sans);
            font-size:0.85rem;
            font-weight:500;
            color:var(--ri-text-tertiary);
        ">No {severity.lower()} findings.</div>
    </div>
    """


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_findings_section(
    findings: list[Finding],
    show_empty_groups: bool = False,
) -> None:
    """
    Render the full Engineering Findings section: findings grouped by
    severity (Critical → High → Medium → Low), each as a premium issue
    card with a severity badge, finding ID, title, message, and a
    visually separated recommendation panel.

    Parameters
    ----------
    findings : list[dict], optional
        Each dict: {"id": str, "severity": str, "title": str,
        "message": str, "recommendation": str}. `severity` should be
        one of "Critical", "High", "Medium", "Low" (unrecognized values
        fall back to a neutral tone and render under no group heading
        adjustment — they're grouped as-is). Defaults to RepoIntel's
        placeholder findings.
    show_empty_groups : bool, default False
        If True, severity groups with zero findings are still rendered
        with a quiet "No findings" placeholder card. By default, empty
        groups are omitted entirely.
    """
    findings = [
        {
            "id": finding.id,
            "severity": finding.severity,
            "title": finding.title,
            "message": finding.message,
            "recommendation": finding.recommendation,
        }
        for finding in findings
    ]

    st.markdown(
        section_title(
            "Engineering Findings",
            "Issues detected during analysis, grouped by severity",
        ),
        unsafe_allow_html=True,
    )

    grouped: dict = {severity: [] for severity in _SEVERITY_ORDER}
    for finding in findings:
        grouped.setdefault(finding.get("severity", "Low"), []).append(finding)

    if not any(grouped.values()):
        st.markdown(
            card(
                """
                <div style="text-align:center; padding:1.25rem 0;">
                    <div style="
                        font-family:var(--ri-font-sans);
                        font-size:0.95rem;
                        font-weight:600;
                        color:var(--ri-text-primary);
                        margin-bottom:0.3rem;
                    ">No findings detected</div>
                    <div style="
                        font-family:var(--ri-font-sans);
                        font-size:0.85rem;
                        color:var(--ri-text-tertiary);
                    ">This repository passed analysis with a clean bill of health.</div>
                </div>
                """,
                hover=False,
            ),
            unsafe_allow_html=True,
        )
        return

    # Render known severities first, in fixed order, then any custom /
    # unrecognized severity labels the caller may have supplied.
    ordered_severities = _SEVERITY_ORDER + [
        s for s in grouped.keys() if s not in _SEVERITY_ORDER
    ]

    for i, severity in enumerate(ordered_severities):
        group = grouped.get(severity, [])

        if not group and not show_empty_groups:
            continue

        if i > 0:
            st.markdown('<div style="height:1.75rem;"></div>', unsafe_allow_html=True)

        st.markdown(_group_heading_html(severity, len(group)), unsafe_allow_html=True)

        if group:
            for finding in group:
                st.markdown(_finding_card_html(finding), unsafe_allow_html=True)
        else:
            st.markdown(_empty_group_html(severity), unsafe_allow_html=True)
