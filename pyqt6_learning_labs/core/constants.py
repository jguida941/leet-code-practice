"""
Application-wide constants and dimensions.
"""

class Dimensions:
    """UI dimensions for consistent sizing."""
    TITLE_BAR_HEIGHT = 45
    CARD_WIDTH = 280
    CARD_HEIGHT = 200
    BUTTON_HEIGHT = 32
    BUTTON_WIDTH = 80
    WINDOW_BUTTON_SIZE = 30
    ICON_CONTAINER_SIZE = 60
    FLOWCHART_NODE_WIDTH = 240
    FLOWCHART_NODE_HEIGHT = 90
    MIN_WINDOW_WIDTH = 800
    MIN_WINDOW_HEIGHT = 600
    DEFAULT_WINDOW_WIDTH = 1200
    DEFAULT_WINDOW_HEIGHT = 800
    RESIZE_MARGIN = 8  # Pixels from edge to trigger resize


class Colors:
    """Theme colors for consistent styling."""
    # Backgrounds
    BG_DARKEST = "#070c1a"
    BG_DARK = "#090d1a"
    BG_MEDIUM = "#0f0a1f"
    BG_CARD = "#1d1142"
    BG_CARD_HOVER = "#2d1b4e"

    # Accents
    ACCENT_PRIMARY = "#a678ff"  # Purple
    ACCENT_SECONDARY = "#00ffae"  # Cyan/Green
    ACCENT_TERTIARY = "#462d7c"  # Dark purple

    # Text
    TEXT_PRIMARY = "#e5f4ff"
    TEXT_SECONDARY = "#8b9bb4"
    TEXT_MUTED = "#5c6370"

    # Semantic
    SUCCESS = "#82d69c"
    ERROR = "#ff5555"
    WARNING = "#f78c6c"

    # Syntax highlighting
    SYNTAX_KEYWORD = "#c792ea"
    SYNTAX_STRING = "#f78c6c"
    SYNTAX_COMMENT = "#82d69c"


class Timing:
    """Animation and timing constants."""
    FADE_DURATION_MS = 200
    DEBOUNCE_MS = 300
    STEP_DELAY_MS = 500
    TOOLTIP_DELAY_MS = 500


class Shortcuts:
    """Keyboard shortcuts."""
    HOME = "Ctrl+H"
    RUN = "Ctrl+R"
    TAB_1 = "Ctrl+1"
    TAB_2 = "Ctrl+2"
    TAB_3 = "Ctrl+3"
    TAB_4 = "Ctrl+4"
    TAB_5 = "Ctrl+5"
    COPY = "Ctrl+C"
    ESCAPE = "Escape"
    STEP_FORWARD = "Ctrl+Right"
    STEP_BACK = "Ctrl+Left"
    RESET = "Ctrl+Shift+R"
