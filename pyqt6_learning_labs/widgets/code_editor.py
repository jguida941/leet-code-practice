from PyQt6.QtCore import Qt, QRegularExpression, QSize, QEvent
from PyQt6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat, QPainter, QTextCursor
from PyQt6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget, QVBoxLayout, QLabel, QCompleter

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
        self.keyword_format.setForeground(QColor("#c792ea"))  # Purple-ish
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#f78c6c"))  # Orange-ish

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#82d69c"))  # Green-ish

    def highlightBlock(self, text: str) -> None:
        for word in self.KEYWORDS:
            expression = QRegularExpression(fr"\\b{word}\\b")
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        string_expr = QRegularExpression(r'"[^"\\]*(?:\\.[^"\\]*)*' r"|'[^'\\]*(?:\\.[^'\\]*)*")
        it = string_expr.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

        comment_index = text.find("#")
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QWidget):
    """
    A reusable code editor widget with syntax highlighting, real-time linting,
    line numbers, and auto-completion.
    """
    def __init__(self, initial_text: str = ""):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.editor = QPlainTextEdit()
        self.editor.setPlainText(initial_text)
        self.editor.setFont(QFont("Courier New", 12))
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0f0a1f;
                color: #e5f4ff;
                border: 2px solid #2d1b4e;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #462d7c;
                selection-color: #ffffff;
            }
            QPlainTextEdit:focus {
                border: 2px solid #a678ff;
            }
        """)
        
        # Setup syntax highlighting
        self.highlighter = PythonHighlighter(self.editor.document())
        
        # Line Numbers
        self.line_number_area = LineNumberArea(self)
        self.editor.blockCountChanged.connect(self.update_line_number_area_width)
        self.editor.updateRequest.connect(self.update_line_number_area)
        self.editor.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

        # Auto-completion
        self.completer = QCompleter(list(PythonHighlighter.KEYWORDS))
        self.completer.setWidget(self.editor)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

        # Install event filter for completer
        self.editor.installEventFilter(self)

        layout.addWidget(self.editor)

        # Syntax status label
        self.syntax_label = QLabel("Syntax: OK")
        self.syntax_label.setStyleSheet("color: #82d69c; font-weight: bold;")
        layout.addWidget(self.syntax_label)

        self._syntax_error_line = None
        self.editor.textChanged.connect(self.lint_code)
        self.editor.textChanged.connect(self.check_completion)
        
        # Initial lint
        self.lint_code()

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
        self.editor.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.editor.viewport().rect()):
            self.update_line_number_area_width(0)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#0f0a1f"))  # Gutter background

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + round(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#5c6370"))  # Line number color
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
            line_color = QColor("#1d1142")  # Current line highlight
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
        if self.completer.popup().isVisible():
            return
            
        completion_prefix = self.text_under_cursor()
        if len(completion_prefix) < 1:  # Trigger after 1 char
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
                return False # Let normal typing happen

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
            self.syntax_label.setStyleSheet("color: #ff5555; font-weight: bold;")
            self._syntax_error_line = exc.lineno
            self.highlight_current_line() # Refresh highlights
            return
        except Exception as exc:
            self.syntax_label.setText(f"Syntax: ERROR {exc}")
            self.syntax_label.setStyleSheet("color: #ff5555; font-weight: bold;")
            self._syntax_error_line = None
            self.highlight_current_line()
            return

        self.syntax_label.setText("Syntax: OK")
        self.syntax_label.setStyleSheet("color: #82d69c; font-weight: bold;")
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
        
        if extra_selections is not None:
             # If we were passed a list, we just append to it, caller handles setting
             pass
        else:
             self.editor.setExtraSelections(extra_selections)

    def has_syntax_error(self) -> bool:
        return self._syntax_error_line is not None
