"""
RepoIntel Design System
========================
A premium Streamlit styling layer inspired by Apple, GitHub, Linear,
Vercel, Cursor, and Raycast.

Principles
----------
- Pure white surfaces, soft neutral-gray cards
- 16-20px rounded corners, soft diffused shadows (no hard borders as crutch)
- Restrained, high-contrast typography using the system UI stack
- Generous whitespace, minimal chrome, no visual noise
- No gradients, no glassmorphism/blur, no neon or saturated accent colors
- Subtle, physical motion (150-220ms, ease-out) on hover/focus only

Usage
-----
    import streamlit as st
    from styles import inject_theme, load_css

    st.set_page_config(page_title="RepoIntel", layout="wide")
    inject_theme()   # sets Streamlit's native theme (page bg, font, etc.)
    load_css()       # injects the full RepoIntel CSS design system

    # Optional helper components:
    from styles import card, badge, divider, section_title, metric_card

This module contains ONLY styling / markup helpers. No app logic,
no page sections, no data — bring your own Streamlit content.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# Design tokens — single source of truth for the whole system
# ---------------------------------------------------------------------------

TOKENS = {
    # Surfaces
    "color-bg": "#FFFFFF",
    "color-surface": "#F7F7F8",          # soft gray card
    "color-surface-hover": "#F1F1F3",
    "color-surface-alt": "#FAFAFA",
    "color-border": "#EAEAEC",
    "color-border-strong": "#E0E0E3",

    # Text
    "color-text-primary": "#111114",
    "color-text-secondary": "#5B5B63",
    "color-text-tertiary": "#8A8A92",
    "color-text-inverse": "#FFFFFF",

    # Accent — one restrained, confident accent (no gradients, no neon)
    "color-accent": "#3D5AFE".replace("#3D5AFE", "#2F6FED"),  # calm indigo-blue
    "color-accent-hover": "#255BD1",
    "color-accent-soft": "#EEF3FE",

    # Semantic
    "color-success": "#1E8E5A",
    "color-success-soft": "#E9F7EF",
    "color-warning": "#B36B00",
    "color-warning-soft": "#FFF4E5",
    "color-danger": "#D33B3B",
    "color-danger-soft": "#FDECEC",

    # Radii
    "radius-sm": "10px",
    "radius-md": "16px",
    "radius-lg": "20px",
    "radius-pill": "999px",

    # Shadows — soft, diffused, low-opacity (never hard drop shadows)
    "shadow-xs": "0 1px 2px rgba(17, 17, 20, 0.04)",
    "shadow-sm": "0 2px 8px rgba(17, 17, 20, 0.05)",
    "shadow-md": "0 6px 20px rgba(17, 17, 20, 0.07)",
    "shadow-lg": "0 16px 40px rgba(17, 17, 20, 0.10)",
    "shadow-focus": "0 0 0 4px rgba(47, 111, 237, 0.14)",

    # Motion
    "ease-out": "cubic-bezier(0.16, 1, 0.3, 1)",
    "duration-fast": "140ms",
    "duration-base": "200ms",

    # Type
    "font-sans": (
        "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro Display', "
        "'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    ),
    "font-mono": (
        "'SF Mono', 'JetBrains Mono', 'Fira Code', ui-monospace, "
        "'Cascadia Code', Menlo, Consolas, monospace"
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def inject_theme() -> None:
    """
    Apply RepoIntel's base Streamlit theme via markdown-injected meta.

    Streamlit's native theme is normally set in .streamlit/config.toml,
    which can't be written from within a running app. This function
    approximates that config by forcing the page background, base font,
    and color-scheme through a very early inline style tag so there is
    no flash of default Streamlit styling before load_css() runs.

    Call this once, immediately after st.set_page_config().
    """
    t = TOKENS
    st.markdown(
        f"""
        <style id="repointel-theme-preboot">
            html {{ color-scheme: light; }}
            body, .stApp {{
                background-color: {t['color-bg']} !important;
                color: {t['color-text-primary']};
                font-family: {t['font-sans']};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_css() -> None:
    """
    Inject the full RepoIntel CSS design system into the current page.

    Idempotent-ish: safe to call once per page render, near the top of
    the script, after inject_theme().
    """
    st.markdown(_build_css(), unsafe_allow_html=True)


def load_fonts(google_fonts: bool = False) -> None:
    """
    Optionally load 'Inter' from Google Fonts as a fallback web font for
    environments where the native system UI font stack (SF Pro / Segoe UI)
    isn't available (e.g. some Linux deployments).

    RepoIntel prefers the OS-native font stack by default (fastest, most
    "native app" feeling — matching Apple/Linear/Raycast conventions), so
    this is opt-in rather than loaded automatically.
    """
    if not google_fonts:
        return
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        </style>
        """,
        unsafe_allow_html=True,
    )


def hide_streamlit_chrome(hide_menu: bool = True, hide_footer: bool = True, hide_header: bool = False) -> None:
    """
    Hide default Streamlit chrome (hamburger menu, 'Made with Streamlit'
    footer, and optionally the top header bar) to reinforce a native,
    branded product feel rather than a generic Streamlit app feel.
    """
    css = "<style>"
    if hide_menu:
        css += "#MainMenu {visibility: hidden;}"
    if hide_footer:
        css += "footer {visibility: hidden;}"
    if hide_header:
        css += "header {visibility: hidden;}"
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Markup helpers — small, composable HTML snippets styled by the CSS above.
# Each returns an HTML string; render with st.markdown(html, unsafe_allow_html=True)
# ---------------------------------------------------------------------------

def card(content_html: str, *, padding: str = "24px", hover: bool = True, className: str = "") -> str:
    """Wrap arbitrary HTML content in a RepoIntel surface card."""
    hover_cls = "ri-card--hover" if hover else ""
    return (
        f'<div class="ri-card {hover_cls} {className}" style="padding:{padding};">'
        f"{content_html}"
        f"</div>"
    )


def metric_card(label: str, value: str, delta: str = "", delta_positive: bool = True) -> str:
    """A compact stat card — number, label, optional delta pill."""
    delta_html = ""
    if delta:
        tone = "ri-pill--success" if delta_positive else "ri-pill--danger"
        delta_html = f'<span class="ri-pill {tone}">{delta}</span>'
    return f"""
    <div class="ri-card ri-card--hover ri-metric">
        <div class="ri-metric__label">{label}</div>
        <div class="ri-metric__row">
            <div class="ri-metric__value">{value}</div>
            {delta_html}
        </div>
    </div>
    """


def badge(text: str, variant: str = "neutral") -> str:
    """
    Small pill badge. variant: 'neutral' | 'accent' | 'success' | 'warning' | 'danger'
    """
    variant_cls = {
        "neutral": "ri-pill--neutral",
        "accent": "ri-pill--accent",
        "success": "ri-pill--success",
        "warning": "ri-pill--warning",
        "danger": "ri-pill--danger",
    }.get(variant, "ri-pill--neutral")
    return f'<span class="ri-pill {variant_cls}">{text}</span>'


def section_title(title: str, subtitle: str = "") -> str:
    """Consistent page/section heading block with tightened tracking."""
    sub = f'<div class="ri-section__subtitle">{subtitle}</div>' if subtitle else ""
    return f"""
    <div class="ri-section">
        <div class="ri-section__title">{title}</div>
        {sub}
    </div>
    """


def divider() -> str:
    """Hairline divider matching the design system's border color."""
    return '<div class="ri-divider"></div>'


def code_pill(text: str) -> str:
    """Inline monospace pill, e.g. for branch names, commit SHAs, file paths."""
    return f'<span class="ri-code-pill">{text}</span>'


def avatar_stack(initials_list, max_visible: int = 4) -> str:
    """Row of overlapping circular initials avatars (e.g. contributors)."""
    visible = initials_list[:max_visible]
    overflow = len(initials_list) - len(visible)
    items = "".join(f'<div class="ri-avatar">{i}</div>' for i in visible)
    if overflow > 0:
        items += f'<div class="ri-avatar ri-avatar--muted">+{overflow}</div>'
    return f'<div class="ri-avatar-stack">{items}</div>'


# ---------------------------------------------------------------------------
# CSS builder
# ---------------------------------------------------------------------------

def _build_css() -> str:
    t = TOKENS
    return f"""
<style>

/* ============================================================
   RepoIntel Design System — root tokens
   ============================================================ */
:root {{
    --ri-bg: {t['color-bg']};
    --ri-surface: {t['color-surface']};
    --ri-surface-hover: {t['color-surface-hover']};
    --ri-surface-alt: {t['color-surface-alt']};
    --ri-border: {t['color-border']};
    --ri-border-strong: {t['color-border-strong']};

    --ri-text-primary: {t['color-text-primary']};
    --ri-text-secondary: {t['color-text-secondary']};
    --ri-text-tertiary: {t['color-text-tertiary']};
    --ri-text-inverse: {t['color-text-inverse']};

    --ri-accent: {t['color-accent']};
    --ri-accent-hover: {t['color-accent-hover']};
    --ri-accent-soft: {t['color-accent-soft']};

    --ri-success: {t['color-success']};
    --ri-success-soft: {t['color-success-soft']};
    --ri-warning: {t['color-warning']};
    --ri-warning-soft: {t['color-warning-soft']};
    --ri-danger: {t['color-danger']};
    --ri-danger-soft: {t['color-danger-soft']};

    --ri-radius-sm: {t['radius-sm']};
    --ri-radius-md: {t['radius-md']};
    --ri-radius-lg: {t['radius-lg']};
    --ri-radius-pill: {t['radius-pill']};

    --ri-shadow-xs: {t['shadow-xs']};
    --ri-shadow-sm: {t['shadow-sm']};
    --ri-shadow-md: {t['shadow-md']};
    --ri-shadow-lg: {t['shadow-lg']};
    --ri-shadow-focus: {t['shadow-focus']};

    --ri-ease: {t['ease-out']};
    --ri-fast: {t['duration-fast']};
    --ri-base: {t['duration-base']};

    --ri-font-sans: {t['font-sans']};
    --ri-font-mono: {t['font-mono']};
}}

/* ============================================================
   Base / reset
   ============================================================ */
html, body, .stApp {{
    background-color: var(--ri-bg) !important;
    color: var(--ri-text-primary);
    font-family: var(--ri-font-sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}}

* {{
    box-sizing: border-box;
}}

/* Kill Streamlit's default green/red accents and default block borders */
.stApp {{
    --primary-color: var(--ri-accent);
}}

.block-container {{
    padding-top: 3.25rem;
    padding-bottom: 4rem;
    max-width: 1180px;
}}

/* Hide default chrome edges for a cleaner canvas */
header[data-testid="stHeader"] {{
    background: transparent;
    backdrop-filter: none;
}}

/* ============================================================
   Typography
   ============================================================ */
h1, h2, h3, h4, h5, h6,
.ri-section__title {{
    font-family: var(--ri-font-sans);
    color: var(--ri-text-primary);
    font-weight: 650;
    letter-spacing: -0.02em;
    line-height: 1.2;
}}

h1 {{ font-size: 2.25rem; letter-spacing: -0.03em; margin-bottom: 0.25rem; }}
h2 {{ font-size: 1.625rem; letter-spacing: -0.025em; }}
h3 {{ font-size: 1.25rem; }}

p, li, span, label, div {{
    font-family: var(--ri-font-sans);
}}

p {{
    color: var(--ri-text-secondary);
    line-height: 1.6;
    font-size: 0.975rem;
}}

code, pre, .stCode {{
    font-family: var(--ri-font-mono) !important;
    font-size: 0.85em;
}}

a {{
    color: var(--ri-accent);
    text-decoration: none;
    transition: color var(--ri-fast) var(--ri-ease);
}}
a:hover {{
    color: var(--ri-accent-hover);
    text-decoration: underline;
}}

/* ============================================================
   Buttons
   ============================================================ */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {{
    background-color: var(--ri-text-primary);
    color: var(--ri-text-inverse);
    border: none;
    border-radius: var(--ri-radius-sm);
    padding: 0.55rem 1.1rem;
    font-weight: 550;
    font-size: 0.9rem;
    letter-spacing: -0.01em;
    box-shadow: var(--ri-shadow-xs);
    transition: transform var(--ri-fast) var(--ri-ease),
                box-shadow var(--ri-fast) var(--ri-ease),
                background-color var(--ri-fast) var(--ri-ease);
}}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {{
    background-color: #262629;
    box-shadow: var(--ri-shadow-sm);
    transform: translateY(-1px);
}}

.stButton > button:active {{
    transform: translateY(0px);
}}

.stButton > button:focus-visible {{
    outline: none;
    box-shadow: var(--ri-shadow-focus);
}}

/* Secondary buttons via kind="secondary" */
button[kind="secondary"] {{
    background-color: var(--ri-surface) !important;
    color: var(--ri-text-primary) !important;
    border: 1px solid var(--ri-border) !important;
    box-shadow: none !important;
}}
button[kind="secondary"]:hover {{
    background-color: var(--ri-surface-hover) !important;
    border-color: var(--ri-border-strong) !important;
}}

/* ============================================================
   Inputs — text, number, select, textarea, date
   ============================================================ */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stDateInput input,
.stTimeInput input {{
    background-color: var(--ri-surface) !important;
    border: 1px solid var(--ri-border) !important;
    border-radius: var(--ri-radius-sm) !important;
    color: var(--ri-text-primary) !important;
    font-size: 0.9rem;
    transition: border-color var(--ri-fast) var(--ri-ease),
                box-shadow var(--ri-fast) var(--ri-ease),
                background-color var(--ri-fast) var(--ri-ease);
}}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus {{
    background-color: var(--ri-bg) !important;
    border-color: var(--ri-accent) !important;
    box-shadow: var(--ri-shadow-focus) !important;
}}

.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {{
    background-color: var(--ri-surface) !important;
    border: 1px solid var(--ri-border) !important;
    border-radius: var(--ri-radius-sm) !important;
    transition: border-color var(--ri-fast) var(--ri-ease);
}}

.stSelectbox div[data-baseweb="select"] > div:hover,
.stMultiSelect div[data-baseweb="select"] > div:hover {{
    border-color: var(--ri-border-strong) !important;
}}

/* Sliders */
.stSlider [data-baseweb="slider"] div[role="slider"] {{
    background-color: var(--ri-accent) !important;
    box-shadow: 0 0 0 4px var(--ri-accent-soft);
}}

/* Checkbox / radio / toggle accents */
.stCheckbox svg, .stRadio svg {{
    color: var(--ri-accent) !important;
}}

[data-testid="stSwitch"] div[data-checked="true"] {{
    background-color: var(--ri-accent) !important;
}}

/* ============================================================
   Tabs
   ============================================================ */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    border-bottom: 1px solid var(--ri-border);
}}

.stTabs [data-baseweb="tab"] {{
    height: auto;
    padding: 0.6rem 1rem;
    color: var(--ri-text-tertiary);
    font-weight: 550;
    font-size: 0.9rem;
    border-radius: var(--ri-radius-sm) var(--ri-radius-sm) 0 0;
    transition: color var(--ri-fast) var(--ri-ease),
                background-color var(--ri-fast) var(--ri-ease);
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: var(--ri-text-primary);
    background-color: var(--ri-surface);
}}

.stTabs [aria-selected="true"] {{
    color: var(--ri-text-primary) !important;
    background-color: transparent !important;
}}

.stTabs [data-baseweb="tab-highlight"] {{
    background-color: var(--ri-text-primary) !important;
    height: 2px;
}}

/* ============================================================
   Expander
   ============================================================ */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary {{
    background-color: var(--ri-surface) !important;
    border-radius: var(--ri-radius-md) !important;
    border: 1px solid var(--ri-border) !important;
    font-weight: 550;
    transition: background-color var(--ri-fast) var(--ri-ease);
}}

[data-testid="stExpander"] summary:hover {{
    background-color: var(--ri-surface-hover) !important;
}}

[data-testid="stExpander"] {{
    border: none !important;
}}

[data-testid="stExpanderDetails"] {{
    background-color: var(--ri-bg);
    border: 1px solid var(--ri-border);
    border-top: none;
    border-radius: 0 0 var(--ri-radius-md) var(--ri-radius-md);
}}

/* ============================================================
   Sidebar
   ============================================================ */
[data-testid="stSidebar"] {{
    background-color: var(--ri-surface-alt);
    border-right: 1px solid var(--ri-border);
}}

[data-testid="stSidebar"] .block-container {{
    padding-top: 2rem;
}}

/* ============================================================
   Dataframe / table
   ============================================================ */
[data-testid="stDataFrame"], .stDataFrame {{
    border: 1px solid var(--ri-border) !important;
    border-radius: var(--ri-radius-md) !important;
    overflow: hidden;
    box-shadow: var(--ri-shadow-xs);
}}

/* ============================================================
   Native metric widget
   ============================================================ */
[data-testid="stMetric"] {{
    background-color: var(--ri-surface);
    border: 1px solid var(--ri-border);
    border-radius: var(--ri-radius-md);
    padding: 1.1rem 1.25rem;
    box-shadow: var(--ri-shadow-xs);
    transition: transform var(--ri-base) var(--ri-ease),
                box-shadow var(--ri-base) var(--ri-ease);
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    box-shadow: var(--ri-shadow-sm);
}}

[data-testid="stMetricValue"] {{
    font-weight: 650;
    letter-spacing: -0.02em;
    color: var(--ri-text-primary);
}}

[data-testid="stMetricLabel"] {{
    color: var(--ri-text-tertiary);
    font-weight: 550;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

/* ============================================================
   Alerts / callouts
   ============================================================ */
.stAlert {{
    border-radius: var(--ri-radius-md) !important;
    border: 1px solid var(--ri-border) !important;
    box-shadow: none !important;
}}

/* ============================================================
   Progress bar
   ============================================================ */
.stProgress > div > div > div {{
    background-color: var(--ri-accent) !important;
    border-radius: var(--ri-radius-pill);
}}
.stProgress > div > div {{
    background-color: var(--ri-surface) !important;
    border-radius: var(--ri-radius-pill);
}}

/* ============================================================
   Scrollbar
   ============================================================ */
::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background-color: var(--ri-border-strong);
    border-radius: var(--ri-radius-pill);
    border: 2px solid var(--ri-bg);
}}
::-webkit-scrollbar-thumb:hover {{
    background-color: #C6C6CC;
}}

/* ============================================================
   Custom RepoIntel components
   ============================================================ */

/* Card */
.ri-card {{
    background-color: var(--ri-surface);
    border: 1px solid var(--ri-border);
    border-radius: var(--ri-radius-lg);
    box-shadow: var(--ri-shadow-xs);
    transition: transform var(--ri-base) var(--ri-ease),
                box-shadow var(--ri-base) var(--ri-ease),
                border-color var(--ri-base) var(--ri-ease);
    animation: ri-fade-in var(--ri-base) var(--ri-ease);
}}

.ri-card--hover:hover {{
    transform: translateY(-3px);
    box-shadow: var(--ri-shadow-md);
    border-color: var(--ri-border-strong);
}}

/* Metric card */
.ri-metric__label {{
    color: var(--ri-text-tertiary);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.045em;
    margin-bottom: 0.4rem;
}}

.ri-metric__row {{
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
}}

.ri-metric__value {{
    font-size: 1.85rem;
    font-weight: 680;
    letter-spacing: -0.02em;
    color: var(--ri-text-primary);
}}

/* Pills / badges */
.ri-pill {{
    display: inline-flex;
    align-items: center;
    padding: 0.22rem 0.65rem;
    border-radius: var(--ri-radius-pill);
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: -0.005em;
    line-height: 1.4;
}}

.ri-pill--neutral {{
    background-color: var(--ri-surface-hover);
    color: var(--ri-text-secondary);
    border: 1px solid var(--ri-border);
}}
.ri-pill--accent {{
    background-color: var(--ri-accent-soft);
    color: var(--ri-accent-hover);
}}
.ri-pill--success {{
    background-color: var(--ri-success-soft);
    color: var(--ri-success);
}}
.ri-pill--warning {{
    background-color: var(--ri-warning-soft);
    color: var(--ri-warning);
}}
.ri-pill--danger {{
    background-color: var(--ri-danger-soft);
    color: var(--ri-danger);
}}

/* Section title block */
.ri-section {{
    margin-bottom: 1.25rem;
}}
.ri-section__title {{
    font-size: 1.375rem;
    font-weight: 650;
    color: var(--ri-text-primary);
}}
.ri-section__subtitle {{
    margin-top: 0.25rem;
    color: var(--ri-text-tertiary);
    font-size: 0.9rem;
}}

/* Divider */
.ri-divider {{
    height: 1px;
    width: 100%;
    background-color: var(--ri-border);
    margin: 1.5rem 0;
    border: none;
}}

/* Code pill (branch, sha, path) */
.ri-code-pill {{
    font-family: var(--ri-font-mono);
    font-size: 0.8rem;
    background-color: var(--ri-surface-hover);
    border: 1px solid var(--ri-border);
    border-radius: 6px;
    padding: 0.1rem 0.45rem;
    color: var(--ri-text-secondary);
}}

/* Avatar stack */
.ri-avatar-stack {{
    display: flex;
    align-items: center;
}}
.ri-avatar {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: var(--ri-text-primary);
    color: var(--ri-text-inverse);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 600;
    border: 2px solid var(--ri-bg);
    margin-left: -8px;
}}
.ri-avatar:first-child {{ margin-left: 0; }}
.ri-avatar--muted {{
    background-color: var(--ri-surface-hover);
    color: var(--ri-text-tertiary);
}}

/* ============================================================
   Motion
   ============================================================ */
@keyframes ri-fade-in {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

@media (prefers-reduced-motion: reduce) {{
    * {{
        animation: none !important;
        transition: none !important;
    }}
}}

</style>
"""
