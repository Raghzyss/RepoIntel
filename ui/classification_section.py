import streamlit as st

from ui.styles import card, badge, section_title
from core.llm.schemas import ProjectClassification


_MATURITY_VARIANTS = {
    "Production-Grade": "success",
    "Mature": "success",
    "Growing": "accent",
    "Emerging": "warning",
    "Experimental": "danger",
    "Early-Stage": "danger",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _maturity_variant(maturity: str) -> str:
    return _MATURITY_VARIANTS.get(maturity, "neutral")


def _confidence_ring_html(confidence: int, size: int = 96, thickness: int = 11) -> str:
    confidence = max(0, min(100, confidence))
    inner = size - thickness * 2
    sweep_deg = round(confidence * 3.6)

    return f"""
    <div style="
        position:relative;
        width:{size}px;
        height:{size}px;
        border-radius:50%;
        background:conic-gradient(
            var(--ri-accent) {sweep_deg}deg,
            var(--ri-surface-hover) {sweep_deg}deg
        );
        display:flex;
        align-items:center;
        justify-content:center;
        flex-shrink:0;
    ">
        <div style="
            width:{inner}px;
            height:{inner}px;
            border-radius:50%;
            background-color:var(--ri-bg);
            box-shadow:var(--ri-shadow-xs);
            display:flex;
            align-items:center;
            justify-content:center;
        ">
            <span style="
                font-family:var(--ri-font-sans);
                font-size:1.2rem;
                font-weight:750;
                letter-spacing:-0.02em;
                color:var(--ri-text-primary);
            ">{confidence}%</span>
        </div>
    </div>
    """


def _eyebrow_html(text: str, extra_style: str = "") -> str:
    return f"""
    <div style="
        font-family:var(--ri-font-sans);
        font-size:0.75rem;
        font-weight:650;
        text-transform:uppercase;
        letter-spacing:0.06em;
        color:var(--ri-text-tertiary);
        {extra_style}
    ">{text}</div>
    """


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_classification_section(classification: ProjectClassification) -> None:

    primary_category = classification.primary_category
    secondary_category = classification.secondary_category

    confidence = (
        round(classification.confidence * 100)
        if classification.confidence <= 1
        else round(classification.confidence)
    )

    engineering_maturity = classification.maturity
    repository_purpose = classification.repository_purpose

    maturity_variant = _maturity_variant(engineering_maturity)

    st.markdown(
        section_title(
            "AI Classification",
            "Model-inferred category, confidence, and repository purpose",
        ),
        unsafe_allow_html=True,
    )

    top_row = f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:2rem;
        flex-wrap:wrap;
    ">
        <div style="flex:1; min-width:240px;">
            {badge("✦ AI Analysis", "accent")}
            {_eyebrow_html("Primary Category", "margin-top:1.1rem;")}
            <div style="
                font-family:var(--ri-font-sans);
                font-size:2.15rem;
                font-weight:750;
                letter-spacing:-0.03em;
                color:var(--ri-text-primary);
                line-height:1.15;
                margin-top:0.3rem;
            ">{primary_category}</div>

            <div style="
                display:flex;
                align-items:center;
                gap:0.55rem;
                margin-top:0.85rem;
            ">
                <span style="
                    font-family:var(--ri-font-sans);
                    font-size:0.78rem;
                    font-weight:600;
                    color:var(--ri-text-tertiary);
                ">Secondary</span>

                {badge(secondary_category, "neutral")}
            </div>
        </div>

        <div style="display:flex; flex-direction:column; align-items:center; gap:0.55rem;">
            {_confidence_ring_html(confidence)}

            <span style="
                font-family:var(--ri-font-sans);
                font-size:0.72rem;
                font-weight:650;
                text-transform:uppercase;
                letter-spacing:0.05em;
                color:var(--ri-text-tertiary);
            ">
                AI Confidence
            </span>
        </div>
    </div>
    """

    maturity_row = f"""
    <div style="display:flex; align-items:center; gap:0.7rem;">
        {_eyebrow_html("Engineering Maturity")}
        {badge(engineering_maturity, maturity_variant)}
    </div>
    """

    purpose_block = f"""
    <div style="
        background-color:var(--ri-surface-hover);
        border:1px solid var(--ri-border);
        border-radius:var(--ri-radius-md);
        padding:18px 20px;
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:0.4rem;
            margin-bottom:0.6rem;
        ">
            <span style="color:var(--ri-accent); font-size:0.85rem;">✦</span>
            {_eyebrow_html("Repository Purpose")}
        </div>

        <div style="
            font-family:var(--ri-font-sans);
            font-size:0.95rem;
            font-weight:450;
            font-style:italic;
            line-height:1.65;
            color:var(--ri-text-secondary);
            letter-spacing:-0.005em;
        ">
            &ldquo;{repository_purpose}&rdquo;
        </div>
    </div>
    """

    divider_html = (
        '<div style="height:1px; background-color:var(--ri-border); '
        'margin:1.5rem 0;"></div>'
    )

    st.markdown(
        card(
            top_row
            + divider_html
            + maturity_row
            + '<div style="height:1.1rem;"></div>'
            + purpose_block,
            padding="26px 28px",
            hover=False,
        ),
        unsafe_allow_html=True,
    )