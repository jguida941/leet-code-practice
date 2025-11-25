from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from pathlib import Path

from pyqt6_learning_labs.core.utils import load_lesson_markdown, markdown_to_html, get_styled_html
from pyqt6_learning_labs.core.constants import Colors


class LessonWidget(QWidget):
    """
    A widget to display markdown lessons with proper HTML rendering.
    """
    def __init__(self, lesson_path: Path, title: str = "Lesson"):
        super().__init__()
        self.lesson_path = lesson_path
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header with title and reload button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 0)

        header = QLabel(title)
        header.setWordWrap(True)
        header.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {Colors.ACCENT_PRIMARY}; margin-bottom: 10px;")
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Reload button
        self.reload_btn = QPushButton("Reload")
        self.reload_btn.setFixedHeight(28)
        self.reload_btn.clicked.connect(lambda: self.reload_lesson(self.lesson_path))
        self.reload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reload_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_CARD};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.ACCENT_TERTIARY};
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_CARD_HOVER};
                border-color: {Colors.ACCENT_SECONDARY};
                color: {Colors.ACCENT_SECONDARY};
            }}
        """)
        header_layout.addWidget(self.reload_btn)

        layout.addLayout(header_layout)

        # Content viewer with HTML support
        self.viewer = QTextBrowser()
        self.viewer.setOpenExternalLinks(True)
        self.viewer.setFont(QFont("JetBrains Mono", 12))
        self.viewer.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {Colors.BG_DARK};
                border: none;
                padding: 10px;
            }}
        """)
        layout.addWidget(self.viewer)

        # Load initial content
        self._load_content(lesson_path)

    def _load_content(self, lesson_path: Path):
        """Load and render markdown content."""
        success, content = load_lesson_markdown(lesson_path)

        if success:
            # Convert markdown to HTML and style it
            html_content = markdown_to_html(content)
            styled_html = get_styled_html(html_content)
            self.viewer.setHtml(styled_html)
        else:
            # Show error message with styling
            error_html = f"""
            <div style="color: {Colors.ERROR}; padding: 20px;">
                <h2>Content Not Available</h2>
                <p>{content}</p>
                <p style="color: {Colors.TEXT_SECONDARY}; margin-top: 20px;">
                    Expected path: <code>{lesson_path}</code>
                </p>
            </div>
            """
            self.viewer.setHtml(get_styled_html(error_html))

    def reload_lesson(self, lesson_path: Path):
        """Reload the lesson content from file."""
        self.lesson_path = lesson_path
        self._load_content(lesson_path)

        # Visual feedback
        original_text = self.reload_btn.text()
        self.reload_btn.setText("Reloaded!")
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.reload_btn.setText(original_text))
