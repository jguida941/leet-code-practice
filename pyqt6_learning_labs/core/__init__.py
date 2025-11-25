"""
Core utilities and configuration for PyQt6 Learning Labs.
"""

from pyqt6_learning_labs.core.constants import Colors, Dimensions, Timing, Shortcuts
from pyqt6_learning_labs.core.theme import set_futuristic_style
from pyqt6_learning_labs.core.utils import (
    load_lesson_markdown,
    markdown_to_html,
    get_styled_html,
    get_base_dir,
    get_lessons_dir
)
from pyqt6_learning_labs.core.safe_exec import (
    safe_exec,
    safe_exec_function,
    check_code_safety,
    CodeSecurityError,
    CodeTimeoutError
)

__all__ = [
    # Constants
    'Colors',
    'Dimensions',
    'Timing',
    'Shortcuts',

    # Theme
    'set_futuristic_style',

    # Utils
    'load_lesson_markdown',
    'markdown_to_html',
    'get_styled_html',
    'get_base_dir',
    'get_lessons_dir',

    # Safe execution
    'safe_exec',
    'safe_exec_function',
    'check_code_safety',
    'CodeSecurityError',
    'CodeTimeoutError',
]
