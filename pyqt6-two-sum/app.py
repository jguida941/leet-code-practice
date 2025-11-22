"""PyQt6 mini learning lab for the Two Sum lesson with styling and interactivity."""
from __future__ import annotations

import math
import sys
import traceback
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from PyQt6.QtCore import Qt, QRegularExpression, QPointF
from PyQt6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPen,
    QPolygonF,
    QSyntaxHighlighter,
    QTextCharFormat,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSlider,
    QSpinBox,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def set_futuristic_style(app: QApplication) -> None:
    """Apply a sci-fi inspired dark theme similar to the sample provided."""
    app.setStyleSheet(
        """
        QWidget {
            background-color: #090d1a;
            color: #e5f4ff;
            font-family: 'Roboto', 'SF Mono', monospace;
            font-size: 14px;
        }
        QLabel {
            color: #bce6ff;
        }
        QPushButton {
            background-color: #111a2c;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #1f2c47;
        }
        QPushButton:hover {
            border: 1px solid #00ffae;
            color: #00ffae;
        }
        QLineEdit, QPlainTextEdit, QTextEdit, QTextBrowser {
            background-color: #0d1526;
            border-radius: 8px;
            border: 1px solid #1f2c47;
            padding: 6px;
        }
        QTabWidget::pane {
            border: 1px solid #162039;
            border-radius: 12px;
        }
        QTabBar::tab {
            background: #111a2c;
            border: 1px solid #162039;
            padding: 8px 14px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        QTabBar::tab:selected {
            background: #14223a;
            color: #00ffae;
        }
        QGroupBox {
            border: 1px solid #1f2c47;
            border-radius: 10px;
            margin-top: 12px;
            padding: 10px;
            background-color: #0d1526;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 4px;
        }
        QSpinBox {
            background: #0d1526;
            border: 1px solid #1f2c47;
            border-radius: 6px;
            padding: 6px;
            min-height: 25px;
        }
        QSlider::groove:horizontal {
            background: #0d1526;
            border: 1px solid #1f2c47;
            border-radius: 6px;
            height: 8px;
        }
        QSlider::handle:horizontal {
            background: #00ffae;
            border: 1px solid #00ffae;
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }
    """
    )


def read_lesson() -> str:
    """Load the Markdown lesson text so the tab stays in sync with the repo."""
    lesson_path = (
        Path(__file__).resolve().parents[1]
        / "two-sum"
        / "python"
        / "lesson"
        / "two-sum-lesson.md"
    )
    if lesson_path.exists():
        return lesson_path.read_text(encoding="utf-8")
    return (
        "Two Sum lesson text missing. Make sure the markdown file exists inside "
        "two-sum/python/lesson."
    )


class PythonHighlighter(QSyntaxHighlighter):
    """Lightweight syntax highlighter for the embedded code editor."""

    KEYWORDS = {
        "and",
        "as",
        "assert",
        "break",
        "class",
        "continue",
        "def",
        "elif",
        "else",
        "except",
        "False",
        "finally",
        "for",
        "from",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "None",
        "not",
        "or",
        "pass",
        "return",
        "True",
        "try",
        "while",
        "with",
        "yield",
    }

    def __init__(self, document):
        super().__init__(document)
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#00ffae"))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#f78c6c"))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#6fbf73"))

    def highlightBlock(self, text: str) -> None:  # noqa: N802
        for word in self.KEYWORDS:
            expression = QRegularExpression(fr"\\b{word}\\b")
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        string_expr = QRegularExpression(
            r'"[^"\\]*(?:\\.[^"\\]*)*' r"|'[^'\\]*(?:\\.[^'\\]*)*"
        )
        it = string_expr.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

        comment_index = text.find("#")
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)


class LessonTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        header = QLabel(
            "Two Sum lesson straight from the repository (read-only so it stays in sync)."
        )
        header.setWordWrap(True)
        layout.addWidget(header)

        viewer = QTextBrowser()
        viewer.setPlainText(read_lesson())
        viewer.setFont(QFont("JetBrains Mono", 11))
        layout.addWidget(viewer)


def two_sum(nums: List[int], target: int) -> Tuple[List[int], List[str]]:
    """Return indices and a textual trace of the algorithm."""
    seen: Dict[int, int] = {}
    steps = [f"Target: {target}", f"Input: {nums}"]

    for index, value in enumerate(nums):
        needed = target - value
        steps.append(f"Index {index}: value={value}, need={needed}")

        if needed in seen:
            steps.append(
                f"Found complement! seen[{needed}]={seen[needed]} so return [{seen[needed]}, {index}]"
            )
            return [seen[needed], index], steps

        seen[value] = index
        steps.append(f"Store {value} -> {index} in dictionary: {seen}")

    steps.append("No pair found that sums to the target.")
    return [], steps


class PlaygroundTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        instructions = QLabel(
            "Edit the list or target, then click Run to see how the dictionary-based"
            " Two Sum scan works step-by-step."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        form_group = QGroupBox("Problem Settings")
        form_layout = QFormLayout(form_group)

        self.list_input = QLineEdit("2, 7, 11, 15")
        self.target_input = QSpinBox()
        self.target_input.setRange(-1_000_000, 1_000_000)
        self.target_input.setValue(9)
        self.target_input.setMinimumWidth(200)
        self.target_input.setMinimumHeight(35)

        form_layout.addRow("Numbers (comma separated)", self.list_input)
        form_layout.addRow("Target", self.target_input)

        layout.addWidget(form_group)

        run_button = QPushButton("Run Two Sum")
        run_button.clicked.connect(self.run_simulation)
        layout.addWidget(run_button)

        self.result_label = QLabel("Result: pending")
        result_font = QFont()
        result_font.setPointSize(12)
        result_font.setBold(True)
        self.result_label.setFont(result_font)
        layout.addWidget(self.result_label)

        self.trace = QTextEdit()
        self.trace.setReadOnly(True)
        self.trace.setMinimumHeight(240)
        layout.addWidget(self.trace)

    def run_simulation(self) -> None:
        try:
            nums = [int(part.strip()) for part in self.list_input.text().split(",") if part.strip()]
        except ValueError:
            self.result_label.setText("Result: WARNING invalid number list")
            self.trace.setPlainText("Make sure every entry is an integer.")
            return

        target = self.target_input.value()
        indices, steps = two_sum(nums, target)
        if indices:
            self.result_label.setText(f"Result: indices {indices}")
        else:
            self.result_label.setText("Result: no pair found")
        self.trace.setPlainText("\n".join(steps))


class FlowchartRect(QGraphicsRectItem):
    WIDTH = 240
    HEIGHT = 90
    BASE_COLOR = QColor("#1b2735")
    ACTIVE_COLOR = QColor("#00c2a8")

    def __init__(
        self,
        title: str,
        detail: str,
        x: int,
        y: int,
        scene: QGraphicsScene,
        on_click: Callable[["FlowchartRect"], None],
    ) -> None:
        super().__init__(x, y, self.WIDTH, self.HEIGHT)
        self.title = title
        self.detail = detail
        self.on_click = on_click
        self.setBrush(self.BASE_COLOR)
        self.setPen(QPen(QColor("#00ffae"), 1))
        self.text_item = scene.addText(title)
        self.text_item.setDefaultTextColor(QColor("#e8f7ff"))
        self.text_item.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        self.text_item.setPos(x + 10, y + 10)
        self.text_item.setZValue(1)
        scene.addItem(self)
        self.setZValue(0)
        self.x_pos = x
        self.y_pos = y

    def set_selected(self, selected: bool) -> None:
        color = self.ACTIVE_COLOR if selected else self.BASE_COLOR
        self.setBrush(color)

    def center_bottom(self) -> Tuple[float, float]:
        return (self.x_pos + self.WIDTH / 2, self.y_pos + self.HEIGHT)

    def center_top(self) -> Tuple[float, float]:
        return (self.x_pos + self.WIDTH / 2, self.y_pos)

    def mousePressEvent(self, event):  # noqa: D401
        if self.on_click:
            self.on_click(self)
        super().mousePressEvent(event)


class FlowchartTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(
            "Interactive flow of the dictionary approach. Click a node to read" " more details."
        )
        label.setWordWrap(True)
        layout.addWidget(label)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-400, -80, 900, 700)
        self.scene.setBackgroundBrush(QColor("#070c1a"))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(self.view, stretch=1)

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)
        self.detail_box.setMinimumHeight(140)
        self.detail_box.setPlainText("Select a step to see what it represents.")
        layout.addWidget(self.detail_box)

        self.nodes: Dict[str, FlowchartRect] = {}
        self.selected: FlowchartRect | None = None
        self._build_graph()

    def _build_graph(self) -> None:
        nodes = {
            "start": (
                "Start + init seen{}",
                "Create an empty dictionary (hash map) to remember values -> indices",
                -280,
                0,
            ),
            "loop": (
                "Loop over nums",
                "Enumerate the array while tracking the current index and value.",
                -40,
                140,
            ),
            "need": (
                "Compute needed",
                "At each step compute target - value to find the complement we still need.",
                -40,
                280,
            ),
            "check": (
                "Is needed stored?",
                "If the complement was seen earlier we can immediately return both indices.",
                -260,
                420,
            ),
            "return": (
                "Return indices",
                "Output the stored index of the complement with the current index and finish.",
                220,
                420,
            ),
            "store": (
                "Store value:index",
                "Otherwise cache value -> index and continue to the next item.",
                -40,
                560,
            ),
        }

        for key, (title, detail, x, y) in nodes.items():
            self.nodes[key] = FlowchartRect(title, detail, x, y, self.scene, self._node_clicked)

        arrows = [
            ("start", "loop"),
            ("loop", "need"),
            ("need", "check"),
            ("check", "return"),
            ("check", "store"),
            ("store", "loop"),
        ]
        for from_id, to_id in arrows:
            self._draw_arrow(self.nodes[from_id], self.nodes[to_id])

    def _draw_arrow(self, start: FlowchartRect, end: FlowchartRect) -> None:
        start_point = start.center_bottom()
        end_point = end.center_top()
        line = self.scene.addLine(
            start_point[0], start_point[1], end_point[0], end_point[1], QPen(QColor("#00ffae"), 2)
        )
        line.setZValue(-1)

        angle = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
        arrow_size = 12
        arrow_p1 = (
            end_point[0] - arrow_size * math.cos(angle - math.pi / 6),
            end_point[1] - arrow_size * math.sin(angle - math.pi / 6),
        )
        arrow_p2 = (
            end_point[0] - arrow_size * math.cos(angle + math.pi / 6),
            end_point[1] - arrow_size * math.sin(angle + math.pi / 6),
        )
        polygon = QPolygonF()
        polygon.append(QPointF(end_point[0], end_point[1]))
        polygon.append(QPointF(arrow_p1[0], arrow_p1[1]))
        polygon.append(QPointF(arrow_p2[0], arrow_p2[1]))
        self.scene.addPolygon(polygon, QPen(QColor("#00ffae")), QColor("#00ffae"))

    def _node_clicked(self, node: FlowchartRect) -> None:
        if self.selected:
            self.selected.set_selected(False)
        node.set_selected(True)
        self.selected = node
        self.detail_box.setPlainText(node.detail)


class ComplexityTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(5, 3))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(5, 200)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.update_plot)
        layout.addWidget(QLabel("Adjust input size to see O(n) work growth:"))
        layout.addWidget(self.slider)

        self.update_plot(self.slider.value())

    def update_plot(self, n: int):
        self.ax.clear()
        x = list(range(1, n + 1))
        y = x
        self.ax.plot(x, y, label="Dictionary scan (O(n))", color="#00ffae")
        self.ax.set_xlabel("Elements in nums")
        self.ax.set_ylabel("Relative work")
        self.ax.set_title("Time complexity")
        self.ax.legend(loc="upper left")
        self.ax.grid(True, linestyle="--", alpha=0.4)
        self.canvas.draw()


TWO_SUM_TEMPLATE = '''def two_sum(nums, target):
    """Return the indices of the two numbers that hit the target."""
    seen = {}
    for i, value in enumerate(nums):
        need = target - value
        if need in seen:
            return [seen[need], i]
        seen[value] = i
    return []
'''


class CodeLabTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        description = QLabel(
            "Write your own function named two_sum(nums, target). Click Run Tests to"
            " check it against curated cases. Syntax is validated live."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        self.editor = QPlainTextEdit()
        self.editor.setPlainText(TWO_SUM_TEMPLATE)
        PythonHighlighter(self.editor.document())
        self.editor.setFont(QFont("JetBrains Mono", 11))
        layout.addWidget(self.editor)

        self.syntax_label = QLabel("Syntax: pending")
        layout.addWidget(self.syntax_label)

        run_button = QPushButton("Run Tests")
        run_button.clicked.connect(self.run_tests)
        layout.addWidget(run_button)

        self.feedback = QTextEdit()
        self.feedback.setReadOnly(True)
        self.feedback.setMinimumHeight(180)
        layout.addWidget(self.feedback)

        self.editor.textChanged.connect(self.lint_code)
        self._syntax_error_line: int | None = None
        self.lint_code()

    def lint_code(self) -> None:
        code = self.editor.toPlainText()
        try:
            compile(code, "<editor>", "exec")
        except SyntaxError as exc:
            self.syntax_label.setText(f"Syntax: ERROR line {exc.lineno} - {exc.msg}")
            self._highlight_error(exc.lineno)
            self._syntax_error_line = exc.lineno
            return
        except Exception as exc:  # noqa: BLE001
            self.syntax_label.setText(f"Syntax: ERROR {exc}")
            self._syntax_error_line = None
            self.editor.setExtraSelections([])
            return

        self.syntax_label.setText("Syntax: OK no compile-time issues detected")
        self._syntax_error_line = None
        self.editor.setExtraSelections([])

    def _highlight_error(self, line: int) -> None:
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(255, 0, 0, 60))
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        for _ in range((line or 1) - 1):
            if not cursor.movePosition(cursor.MoveOperation.Down):
                break
        cursor.select(cursor.SelectionType.LineUnderCursor)
        selection.cursor = cursor
        self.editor.setExtraSelections([selection])

    def run_tests(self) -> None:
        if self._syntax_error_line is not None:
            self.feedback.setPlainText(
                f"Fix syntax error on line {self._syntax_error_line} before running tests."
            )
            return

        code = self.editor.toPlainText()
        namespace: Dict[str, object] = {}
        try:
            exec(code, namespace)
        except Exception as exc:  # noqa: BLE001
            self.feedback.setPlainText(f"Code error: {exc}\n{traceback.format_exc()}")
            return

        func = namespace.get("two_sum")
        if not callable(func):
            self.feedback.setPlainText("Define a function named two_sum(nums, target).")
            return

        cases = [
            ([2, 7, 11, 15], 9, [0, 1]),
            ([3, 3], 6, [0, 1]),
            ([3, 2, 4], 6, [1, 2]),
            ([1, 2, 3, 4, 5, 6], 11, [4, 5]),
        ]

        report_lines: List[str] = []
        for nums, target, expected in cases:
            try:
                answer = func(list(nums), target)
            except Exception as exc:  # noqa: BLE001
                self.feedback.setPlainText(
                    f"Runtime error for nums={nums}, target={target}: {exc}\n{traceback.format_exc()}"
                )
                return

            if answer != expected:
                self.feedback.setPlainText(
                    "Wrong answer for nums={0}, target={1}. Expected {2}, got {3}".format(
                        nums, target, expected, answer
                    )
                )
                return
            report_lines.append(f"PASS nums={nums}, target={target} -> {answer}")

        self.feedback.setPlainText("\n".join(report_lines) + "\nAll tests passed!")


class TwoSumWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Two Sum Learning Lab")
        tabs = QTabWidget()
        tabs.addTab(LessonTab(), "Lesson")
        tabs.addTab(PlaygroundTab(), "Playground")
        tabs.addTab(FlowchartTab(), "Flowchart")
        tabs.addTab(ComplexityTab(), "Complexity")
        tabs.addTab(CodeLabTab(), "Code Lab")
        self.setCentralWidget(tabs)
        self.resize(1024, 760)


def main() -> None:
    app = QApplication(sys.argv)
    set_futuristic_style(app)
    window = TwoSumWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
