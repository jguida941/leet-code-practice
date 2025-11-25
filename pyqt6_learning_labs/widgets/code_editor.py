from PyQt6.QtCore import Qt, QRegularExpression, QSize, QEvent, QTimer, QRect
from PyQt6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat, QPainter, QTextCursor, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QPlainTextEdit, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCompleter, QPushButton, QApplication
)

from pyqt6_learning_labs.core.constants import Colors, Timing


class PythonHighlighter(QSyntaxHighlighter):
    """Lightweight syntax highlighter for Python code."""
    KEYWORDS = {
        "and", "as", "assert", "break", "class", "continue", "def",
        "elif", "else", "except", "False", "finally", "for", "from",
        "if", "import", "in", "is", "lambda", "None", "not", "or",
        "pass", "return", "True", "try", "while", "with", "yield",
    }

    def __init__(self, document):
        super().__init__(document)
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(Colors.SYNTAX_KEYWORD))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(Colors.SYNTAX_STRING))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(Colors.SYNTAX_COMMENT))

        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(Colors.ACCENT_SECONDARY))

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(Colors.WARNING))

    def highlightBlock(self, text: str) -> None:
        # Keywords
        for word in self.KEYWORDS:
            expression = QRegularExpression(fr"\\b{word}\\b")
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        # Function definitions
        func_expr = QRegularExpression(r"\bdef\s+(\w+)")
        it = func_expr.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.function_format)

        # Numbers
        num_expr = QRegularExpression(r"\b\d+\.?\d*\b")
        it = num_expr.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)

        # Strings
        string_expr = QRegularExpression(r'"[^"\\]*(?:\\.[^"\\]*)*' r"|'[^'\\]*(?:\\.[^'\\]*)*")
        it = string_expr.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

        # Comments
        comment_index = text.find("#")
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)


class LineNumberArea(QWidget):
    def __init__(self, text_edit, code_editor):
        super().__init__(text_edit)
        self.text_edit = text_edit
        self.code_editor = code_editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QWidget):
    """
    A reusable code editor widget with syntax highlighting, real-time linting,
    line numbers, auto-completion, and copy functionality.
    """
    def __init__(self, initial_text: str = ""):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Toolbar with copy button
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)

        self.copy_btn = QPushButton("Copy Code")
        self.copy_btn.setFixedHeight(28)
        self.copy_btn.clicked.connect(self.copy_code)
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.setAccessibleName("Copy code to clipboard")
        self.copy_btn.setStyleSheet(f"""
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
        toolbar.addStretch()
        toolbar.addWidget(self.copy_btn)
        layout.addLayout(toolbar)

        self.editor = QPlainTextEdit()
        self.editor.setPlainText(initial_text)
        self.editor.setFont(QFont("Courier New", 12))
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {Colors.BG_MEDIUM};
                color: {Colors.TEXT_PRIMARY};
                border: 2px solid {Colors.BG_CARD_HOVER};
                border-radius: 6px;
                padding: 8px;
                selection-background-color: {Colors.ACCENT_TERTIARY};
                selection-color: #ffffff;
            }}
            QPlainTextEdit:focus {{
                border: 2px solid {Colors.ACCENT_PRIMARY};
            }}
        """)

        # Setup syntax highlighting
        self.highlighter = PythonHighlighter(self.editor.document())

        # Line Numbers - must be child of editor for proper positioning
        self.line_number_area = LineNumberArea(self.editor, self)
        self.editor.blockCountChanged.connect(self.update_line_number_area_width)
        self.editor.updateRequest.connect(self.update_line_number_area)
        self.editor.cursorPositionChanged.connect(self.highlight_current_line)

        # Handle resize to position line number area
        self._original_resize_event = self.editor.resizeEvent
        self.editor.resizeEvent = self._on_editor_resize

        self.update_line_number_area_width(0)

        # Auto-completion
        self.completer = QCompleter(list(PythonHighlighter.KEYWORDS))
        self.completer.setWidget(self.editor)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

        # Install event filter for completer
        self.editor.installEventFilter(self)

        # Hide completion popup when editor loses focus
        self.editor.focusOutEvent = self._on_focus_out

        layout.addWidget(self.editor)

        # Syntax status label
        self.syntax_label = QLabel("Syntax: OK")
        self.syntax_label.setStyleSheet(f"color: {Colors.SUCCESS}; font-weight: bold;")
        layout.addWidget(self.syntax_label)

        self._syntax_error_line = None

        # Debounced linting
        self._lint_timer = QTimer()
        self._lint_timer.setSingleShot(True)
        self._lint_timer.timeout.connect(self._do_lint)

        self._completion_timer = QTimer()
        self._completion_timer.setSingleShot(True)
        self._completion_timer.timeout.connect(self._do_check_completion)

        self.editor.textChanged.connect(self._schedule_lint)
        self.editor.textChanged.connect(self._schedule_completion)

        # Initial lint
        self._do_lint()

    def _on_focus_out(self, event):
        """Hide completion popup when editor loses focus."""
        self.completer.popup().hide()
        QPlainTextEdit.focusOutEvent(self.editor, event)

    def _on_editor_resize(self, event):
        """Handle editor resize to reposition line number area."""
        self._original_resize_event(event)
        cr = self.editor.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def copy_code(self):
        """Copy the current code to clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.editor.toPlainText())
        # Visual feedback
        original_text = self.copy_btn.text()
        self.copy_btn.setText("Copied!")
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT_SECONDARY};
                color: {Colors.BG_DARK};
                border: 1px solid {Colors.ACCENT_SECONDARY};
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: bold;
            }}
        """)
        QTimer.singleShot(1500, lambda: self._reset_copy_button(original_text))

    def _reset_copy_button(self, original_text):
        """Reset copy button to original state."""
        self.copy_btn.setText(original_text)
        self.copy_btn.setStyleSheet(f"""
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

    def _schedule_lint(self):
        """Schedule a lint operation with debouncing."""
        self._lint_timer.start(Timing.DEBOUNCE_MS)

    def _schedule_completion(self):
        """Schedule completion check with debouncing."""
        # Only schedule if editor is visible and focused
        if not self.isVisible() or not self.editor.hasFocus():
            return
        if not self.completer.popup().isVisible():
            self._completion_timer.start(Timing.DEBOUNCE_MS)

    def _do_lint(self):
        """Perform the actual lint operation."""
        self.lint_code()

    def _do_check_completion(self):
        """Perform the actual completion check."""
        self.check_completion()

    # --- Line Numbers Logic ---
    def line_number_area_width(self):
        digits = 1
        max_value = max(1, self.editor.blockCount())
        while max_value >= 10:
            max_value //= 10
            digits += 1
        space = 3 + self.editor.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        width = self.line_number_area_width()
        self.editor.setViewportMargins(width, 0, 0, 0)
        # Update line number area geometry
        cr = self.editor.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), width, cr.height()))

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.editor.viewport().rect()):
            self.update_line_number_area_width(0)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(Colors.BG_MEDIUM))

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + round(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(Colors.TEXT_MUTED))
                painter.drawText(0, top, self.line_number_area.width() - 2, self.editor.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + round(self.editor.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.editor.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Colors.BG_CARD)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            selection.cursor = self.editor.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        # Re-add syntax error highlight if exists
        if self._syntax_error_line is not None:
            self._highlight_error(self._syntax_error_line, extra_selections)
        else:
            self.editor.setExtraSelections(extra_selections)

    # --- Auto-completion Logic ---
    def insert_completion(self, completion):
        tc = self.editor.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Left)
        tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
        tc.insertText(completion[-extra:])
        self.editor.setTextCursor(tc)

    def text_under_cursor(self):
        tc = self.editor.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        return tc.selectedText()

    def check_completion(self):
        # Don't show completion if editor isn't visible or focused
        if not self.isVisible() or not self.editor.hasFocus():
            return

        if self.completer.popup().isVisible():
            return

        completion_prefix = self.text_under_cursor()
        if len(completion_prefix) < 1:
            return

        if completion_prefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completion_prefix)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.editor.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def eventFilter(self, obj, event):
        if obj == self.editor and event.type() == QEvent.Type.KeyPress:
            if self.completer.popup().isVisible():
                if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape, Qt.Key.Key_Tab, Qt.Key.Key_Backtab):
                    event.ignore()
                    return True

            is_shortcut = (event.modifiers() & Qt.KeyboardModifier.ControlModifier) and event.key() == Qt.Key.Key_Space
            if not self.completer.popup().isVisible() and not is_shortcut:
                return False

            # Ctrl+Space to force complete
            if is_shortcut:
                self.check_completion()
                return True

        return super().eventFilter(obj, event)

    # --- Existing Logic ---
    def get_code(self) -> str:
        return self.editor.toPlainText()

    def set_code(self, code: str):
        self.editor.setPlainText(code)

    def lint_code(self):
        code = self.editor.toPlainText()
        try:
            compile(code, "<editor>", "exec")
        except SyntaxError as exc:
            self.syntax_label.setText(f"Syntax: ERROR line {exc.lineno} - {exc.msg}")
            self.syntax_label.setStyleSheet(f"color: {Colors.ERROR}; font-weight: bold;")
            self._syntax_error_line = exc.lineno
            self.highlight_current_line()
            return
        except Exception as exc:
            self.syntax_label.setText(f"Syntax: ERROR {exc}")
            self.syntax_label.setStyleSheet(f"color: {Colors.ERROR}; font-weight: bold;")
            self._syntax_error_line = None
            self.highlight_current_line()
            return

        self.syntax_label.setText("Syntax: OK")
        self.syntax_label.setStyleSheet(f"color: {Colors.SUCCESS}; font-weight: bold;")
        self._syntax_error_line = None
        self.highlight_current_line()

    def _highlight_error(self, line: int, extra_selections=None):
        if extra_selections is None:
            extra_selections = []

        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(255, 0, 0, 60))
        selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)

        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        for _ in range((line or 1) - 1):
            if not cursor.movePosition(cursor.MoveOperation.Down):
                break
        cursor.select(cursor.SelectionType.LineUnderCursor)
        selection.cursor = cursor
        extra_selections.append(selection)

        self.editor.setExtraSelections(extra_selections)

    def has_syntax_error(self) -> bool:
        return self._syntax_error_line is not None
