"""
Reusable widget components for PyQt6 Learning Labs.
"""

from pyqt6_learning_labs.widgets.code_editor import CodeEditor, PythonHighlighter
from pyqt6_learning_labs.widgets.complexity import ComplexityWidget, SimplePlotWidget
from pyqt6_learning_labs.widgets.flowchart import FlowchartWidget, FlowchartNode
from pyqt6_learning_labs.widgets.lesson import LessonWidget

__all__ = [
    # Code Editor
    'CodeEditor',
    'PythonHighlighter',

    # Complexity
    'ComplexityWidget',
    'SimplePlotWidget',

    # Flowchart
    'FlowchartWidget',
    'FlowchartNode',

    # Lesson
    'LessonWidget',
]
