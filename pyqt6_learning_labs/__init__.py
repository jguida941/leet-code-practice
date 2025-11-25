"""
PyQt6 Learning Labs - Interactive Algorithm Learning Platform

A comprehensive educational application for learning algorithms through
interactive visualizations, step-by-step execution, and hands-on coding.
"""

__version__ = "2.1.0"
__author__ = "LeetCode Practice"

# Re-export main components for easy access
from pyqt6_learning_labs.core import (
    Colors,
    Dimensions,
    Timing,
    Shortcuts,
    set_futuristic_style,
)

from pyqt6_learning_labs.widgets import (
    CodeEditor,
    ComplexityWidget,
    FlowchartWidget,
    LessonWidget,
)

__all__ = [
    # Version info
    '__version__',
    '__author__',

    # Core constants
    'Colors',
    'Dimensions',
    'Timing',
    'Shortcuts',
    'set_futuristic_style',

    # Widgets
    'CodeEditor',
    'ComplexityWidget',
    'FlowchartWidget',
    'LessonWidget',
]
