# ===============================
# THEME DEFINITIONS
# ===============================

THEMES = {
    "dark": {
        "bg": "#0f1115",
        "header": "#1e1e1e",
        "card": "#161a22",
        "card_hover": "#1f2937",
        "accent": "#00ccff",
        "accent_dark": "#0f3460",
        "text": "#eaeaea",
        "muted": "#9ca3af",
        "panel": "#1A2230",
        "status": "#1e1e1e",
    },

    "light": {
        "bg": "#f4f6f9",
        "header": "#ffffff",
        "card": "#ffffff",
        "card_hover": "#e5e7eb",
        "accent": "#2563eb",
        "accent_dark": "#1d4ed8",
        "text": "#111827",
        "muted": "#6b7280",
        "panel": "#f1f5f9",
        "status": "#ffffff",
    }
}

# ===============================
# CURRENT THEME
# ===============================

CURRENT_THEME = "dark"

# ===============================
# BACKWARD COMPATIBILITY
# (Your existing code uses COLORS)
# ===============================

COLORS = THEMES[CURRENT_THEME]

# ===============================
# FONTS
# ===============================

FONTS = {
    "title": ("Segoe UI", 28, "bold"),
    "card": ("Segoe UI", 11, "bold"),
    "small": ("Segoe UI", 10),
    "section": ("Segoe UI", 12, "bold"),
}

# ===============================
# BUTTON COLORS
# ===============================

BUTTONS = {
    "primary": "#2563eb",
    "danger": "#dc2626",
    "success": "#16a34a",
    "secondary": "#334155",
}

# ===============================
# SIZES
# ===============================

SIZES = {
    "header_h": 70,
}
