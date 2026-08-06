# ==========================================================
# Domain Budgets
# ==========================================================

DOMAIN_BUDGETS = {

    "Documentation": 20,

    "Structure": 15,

    "Code": 25,

    "Dependency": 10,

    "Security": 20,

    "Health": 10,

}


# ==========================================================
# Base Weights
# ==========================================================

BASE_WEIGHTS = {

    # ======================================================
    # Documentation
    # ======================================================

    "DOC001": {"domain": "Documentation", "deduction": 15},
    "DOC002": {"domain": "Documentation", "deduction": 5},
    "DOC003": {"domain": "Documentation", "deduction": 3},
    "DOC004": {"domain": "Documentation", "deduction": 3},
    "DOC005": {"domain": "Documentation", "deduction": 2},
    "DOC006": {"domain": "Documentation", "deduction": 1},
    "DOC007": {"domain": "Documentation", "deduction": 2},

    # ======================================================
    # Structure
    # ======================================================

    "STR001": {"domain": "Structure", "deduction": 2},
    "STR002": {"domain": "Structure", "deduction": 2},
    "STR003": {"domain": "Structure", "deduction": 2},
    "STR004": {"domain": "Structure", "deduction": 2},
    "STR005": {"domain": "Structure", "deduction": 4},
    "STR006": {"domain": "Structure", "deduction": 2},
    "STR007": {"domain": "Structure", "deduction": 2},
    "STR008": {"domain": "Structure", "deduction": 2},
    "STR009": {"domain": "Structure", "deduction": 6},
    "STR010": {"domain": "Structure", "deduction": 1},

    # ======================================================
    # Code
    # ======================================================

    "CODE001": {"domain": "Code", "deduction": 3},
    "CODE002": {"domain": "Code", "deduction": 6},
    "CODE003": {"domain": "Code", "deduction": 3},
    "CODE004": {"domain": "Code", "deduction": 2},
    "CODE005": {"domain": "Code", "deduction": 3},
    "CODE006": {"domain": "Code", "deduction": 2},
    "CODE007": {"domain": "Code", "deduction": 2},
    "CODE008": {"domain": "Code", "deduction": 3},
    "CODE009": {"domain": "Code", "deduction": 2},
    "CODE010": {"domain": "Code", "deduction": 2},
    "CODE011": {"domain": "Code", "deduction": 2},
    "CODE012": {"domain": "Code", "deduction": 2},
    "CODE013": {"domain": "Code", "deduction": 4},

    # ======================================================
    # Dependency
    # ======================================================

    "DEP001": {"domain": "Dependency", "deduction": 4},
    "DEP002": {"domain": "Dependency", "deduction": 5},
    "DEP003": {"domain": "Dependency", "deduction": 3},
    "DEP004": {"domain": "Dependency", "deduction": 2},
    "DEP005": {"domain": "Dependency", "deduction": 2},
    "DEP006": {"domain": "Dependency", "deduction": 2},

    # ======================================================
    # Security
    # ======================================================

    "SEC001": {"domain": "Security", "deduction": 10},
    "SEC002": {"domain": "Security", "deduction": 10},
    "SEC003": {"domain": "Security", "deduction": 8},
    "SEC004": {"domain": "Security", "deduction": 8},
    "SEC005": {"domain": "Security", "deduction": 8},
    "SEC006": {"domain": "Security", "deduction": 4},
    "SEC007": {"domain": "Security", "deduction": 3},
    "SEC008": {"domain": "Security", "deduction": 8},
    "SEC009": {"domain": "Security", "deduction": 8},

    # ======================================================
    # Health
    # ======================================================

    "HLTH001": {"domain": "Health", "deduction": 2},
    "HLTH002": {"domain": "Health", "deduction": 2},
    "HLTH003": {"domain": "Health", "deduction": 2},
    "HLTH004": {"domain": "Health", "deduction": 2},
    "HLTH005": {"domain": "Health", "deduction": 2},
    "HLTH006": {"domain": "Health", "deduction": 5},
    "HLTH007": {"domain": "Health", "deduction": 4},
    "HLTH008": {"domain": "Health", "deduction": 4},

}


# ==========================================================
# Category Override Deltas
# ==========================================================

CATEGORY_OVERRIDES = {

    "WEB_APPLICATION": {

        "HLTH008": 4,
        "SEC007": 2,

    },

    "LIBRARY_FRAMEWORK": {

        "HLTH008": -4,
        "SEC007": -3,

    },

    "API_BACKEND_SERVICE": {

        "HLTH008": 3,
        "SEC007": 2,

    },

    "AI_ML_PROJECT": {

        "HLTH008": -2,

    },

    "CLI_DEVELOPER_TOOL": {

        "HLTH008": -4,

    },

    "MOBILE_DESKTOP_APPLICATION": {

        "HLTH008": -3,

    },

}

# ==========================================================
# Domain Attribute Mapping
# ==========================================================

DOMAIN_MAP = {

    "Documentation": "documentation",

    "Structure": "structure",

    "Code": "code",

    "Dependency": "dependency",

    "Security": "security",

    "Health": "health",

}