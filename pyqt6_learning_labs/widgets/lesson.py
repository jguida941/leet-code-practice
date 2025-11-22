from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
from PyQt6.QtGui import QFont
from pathlib import Path
from pyqt6_learning_labs.core.utils import load_lesson_markdown

class LessonWidget(QWidget):
    """
    A widget to display markdown lessons.
    """
    def __init__(self, lesson_path: Path, title: str = "Lesson"):
        super().__init__()
        layout = QVBoxLayout(self)
        
        header = QLabel(title)
        header.setWordWrap(True)
        header.setStyleSheet("font-weight: bold; font-size: 16px; color: #a678ff; margin-bottom: 10px;")
        layout.addWidget(header)

        self.viewer = QTextBrowser()
        self.viewer.setPlainText(load_lesson_markdown(lesson_path))
        self.viewer.setFont(QFont("JetBrains Mono", 12))
        layout.addWidget(self.viewer)

    def reload_lesson(self, lesson_path: Path):
        self.viewer.setPlainText(load_lesson_markdown(lesson_path))
