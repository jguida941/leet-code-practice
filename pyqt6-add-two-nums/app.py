"""PyQt6 companion app for the Add Two Numbers lesson with styling and tooling."""
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


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def set_futuristic_style(app: QApplication) -> None:
    """Apply a consistent sci-fi theme shared with the Two Sum lab."""
    app.setStyleSheet(
        """
        QWidget {
            background-color: #090d1a;
            color: #e5f4ff;
            font-family: 'Roboto', 'SF Mono', monospace;
            font-size: 14px;
        }
        QLabel { color: #d7c6ff; }
        QPushButton {
            background-color: #11112c;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #462d7c;
        }
        QPushButton:hover {
            border: 1px solid #a678ff;
            color: #a678ff;
        }
        QLineEdit, QPlainTextEdit, QTextEdit, QTextBrowser {
            background-color: #120c24;
            border-radius: 8px;
            border: 1px solid #462d7c;
            padding: 6px;
        }
        QGroupBox {
            border: 1px solid #462d7c;
            border-radius: 10px;
            margin-top: 12px;
            padding: 10px;
            background-color: #0f0a1f;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 4px;
        }
        QTabWidget::pane {
            border: 1px solid #462d7c;
            border-radius: 12px;
        }
        QTabBar::tab {
            background: #11112c;
            border: 1px solid #462d7c;
            padding: 8px 14px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        QTabBar::tab:selected {
            background: #1d1142;
            color: #d8b5ff;
        }
        QSpinBox {
            background: #120c24;
            border: 1px solid #462d7c;
            border-radius: 6px;
            padding: 6px;
            min-height: 25px;
        }
        QSlider::groove:horizontal {
            background: #120c24;
            border: 1px solid #462d7c;
            border-radius: 6px;
            height: 8px;
        }
        QSlider::handle:horizontal {
            background: #d8b5ff;
            border: 1px solid #d8b5ff;
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }
    """
    )


def list_to_nodes(values: List[int]) -> ListNode | None:
    dummy = ListNode()
    cur = dummy
    for value in values:
        cur.next = ListNode(value)
        cur = cur.next
    return dummy.next


def nodes_to_list(head: ListNode | None) -> List[int]:
    out: List[int] = []
    cur = head
    while cur:
        out.append(cur.val)
        cur = cur.next
    return out


def load_lesson() -> str:
    lesson_path = (
        Path(__file__).resolve().parents[1]
        / "add-two-numbers"
        / "lesson"
        / "add-two-nums.md"
    )
    if lesson_path.exists():
        return lesson_path.read_text(encoding="utf-8")
    return "Lesson file missing in add-two-numbers/lesson/add-two-nums.md"


class PythonHighlighter(QSyntaxHighlighter):
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
        self.keyword_format.setForeground(QColor("#c792ea"))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#82d69c"))

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#f78c6c"))

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
        label = QLabel("Fresh copy of the add-two-numbers lesson for quick review.")
        label.setWordWrap(True)
        layout.addWidget(label)

        viewer = QTextBrowser()
        viewer.setPlainText(load_lesson())
        viewer.setFont(QFont("JetBrains Mono", 11))
        layout.addWidget(viewer)


def add_two_numbers_with_trace(
    l1: List[int], l2: List[int], base: int = 10
) -> Tuple[List[int], List[str]]:
    node1 = list_to_nodes(l1)
    node2 = list_to_nodes(l2)

    dummy = ListNode()
    cur = dummy
    carry = 0
    step = 0
    trace: List[str] = [f"Input A: {l1}", f"Input B: {l2}", f"Base: {base}"]

    while node1 or node2 or carry:
        v1 = node1.val if node1 else 0
        v2 = node2.val if node2 else 0
        carry_in = carry
        total = v1 + v2 + carry_in
        carry = total // base
        digit = total % base
        trace.append(
            f"Step {step}: v1={v1}, v2={v2}, carry in={carry_in}, total={total}, "
            f"write digit={digit}, carry out={carry}"
        )
        cur.next = ListNode(digit)
        cur = cur.next
        node1 = node1.next if node1 else None
        node2 = node2.next if node2 else None
        step += 1

    result = nodes_to_list(dummy.next)
    trace.append(f"Result digits (reverse order): {result}")
    return result, trace


class PlaygroundTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        instructions = QLabel(
            "Enter digits for each linked list (least-significant digit first)."
            " The simulator shows the resulting list and decimal value."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        form_group = QGroupBox("Linked list inputs")
        form_layout = QFormLayout(form_group)
        self.list1 = QLineEdit("2, 4, 3")
        self.list2 = QLineEdit("5, 6, 4")
        self.base_spin = QSpinBox()
        self.base_spin.setRange(2, 10)
        self.base_spin.setValue(10)
        self.base_spin.setMinimumWidth(200)
        self.base_spin.setMinimumHeight(35)

        form_layout.addRow("List A digits", self.list1)
        form_layout.addRow("List B digits", self.list2)
        form_layout.addRow("Base", self.base_spin)
        layout.addWidget(form_group)

        run_button = QPushButton("Add Numbers")
        run_button.clicked.connect(self.run_addition)
        layout.addWidget(run_button)

        self.result_label = QLabel("Result digits: ?")
        bold = QFont()
        bold.setPointSize(11)
        bold.setBold(True)
        self.result_label.setFont(bold)
        layout.addWidget(self.result_label)

        self.decimal_label = QLabel("Decimal values: ?")
        layout.addWidget(self.decimal_label)

        self.trace_box = QTextEdit()
        self.trace_box.setReadOnly(True)
        self.trace_box.setMinimumHeight(220)
        layout.addWidget(self.trace_box)

    def parse_digits(self, text: str) -> List[int] | None:
        try:
            digits = [int(part.strip()) for part in text.split(",") if part.strip()]
        except ValueError:
            return None
        if any(digit >= self.base_spin.value() or digit < 0 for digit in digits):
            return None
        return digits or [0]

    def to_decimal(self, digits: List[int]) -> int:
        base = self.base_spin.value()
        value = 0
        multiplier = 1
        for digit in digits:
            value += digit * multiplier
            multiplier *= base
        return value

    def run_addition(self):
        digits_a = self.parse_digits(self.list1.text())
        digits_b = self.parse_digits(self.list2.text())
        if digits_a is None or digits_b is None:
            self.result_label.setText("Result digits: WARNING invalid digits for base")
            self.decimal_label.setText("Decimal values: --")
            self.trace_box.setPlainText(
                "Check that digits are integers and smaller than the selected base."
            )
            return

        base = self.base_spin.value()
        result, trace = add_two_numbers_with_trace(digits_a, digits_b, base)
        self.result_label.setText(f"Result digits (reverse order): {result}")
        dec_a = self.to_decimal(digits_a)
        dec_b = self.to_decimal(digits_b)
        dec_sum = self.to_decimal(result)
        self.decimal_label.setText(
            f"Decimal A={dec_a}, B={dec_b}, Sum={dec_sum}"
        )
        self.trace_box.setPlainText("\n".join(trace))


class FlowchartRect(QGraphicsRectItem):
    WIDTH = 260
    HEIGHT = 90
    BASE_COLOR = QColor("#2a1b47")
    ACTIVE_COLOR = QColor("#a678ff")

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
        self.setPen(QPen(QColor("#c8a4ff"), 1))
        self.text_item = scene.addText(title)
        self.text_item.setDefaultTextColor(QColor("#f5e5ff"))
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

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self)
        super().mousePressEvent(event)


class FlowchartTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(
            "Interactive carry-propagation flow. Click any state for an in-depth description."
        )
        label.setWordWrap(True)
        layout.addWidget(label)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-420, -80, 960, 740)
        self.scene.setBackgroundBrush(QColor("#070714"))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(self.view, stretch=1)

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)
        self.detail_box.setMinimumHeight(140)
        self.detail_box.setPlainText("Select a step to learn what happens in that stage.")
        layout.addWidget(self.detail_box)

        self.nodes: Dict[str, FlowchartRect] = {}
        self.selected: FlowchartRect | None = None
        self._build_graph()

    def _build_graph(self):
        nodes = {
            "start": (
                "Start + dummy",
                "Create a dummy head + carry=0 so appending nodes is uniform.",
                -260,
                0,
            ),
            "read": (
                "Read digits",
                "Pull v1/v2 from the current l1/l2 nodes (or 0 if we've run out).",
                100,
                120,
            ),
            "sum": (
                "Compute total",
                "Add v1 + v2 + carry to get the raw sum for this column.",
                100,
                260,
            ),
            "split": (
                "Split digit/carry",
                "digit = total % base, carry = total // base.",
                -260,
                400,
            ),
            "append": (
                "Append digit",
                "Create a node containing digit and hook it to the running list.",
                220,
                400,
            ),
            "advance": (
                "Advance pointers",
                "Move l1/l2 (if they exist) and repeat until no digits and carry=0.",
                -20,
                560,
            ),
            "done": (
                "Return dummy.next",
                "Return the list beginning after the dummy node for the real answer.",
                -20,
                700,
            ),
        }

        for key, (title, detail, x, y) in nodes.items():
            self.nodes[key] = FlowchartRect(title, detail, x, y, self.scene, self._node_clicked)

        arrows = [
            ("start", "read"),
            ("read", "sum"),
            ("sum", "split"),
            ("sum", "append"),
            ("split", "append"),
            ("append", "advance"),
            ("advance", "read"),
            ("advance", "done"),
        ]
        for from_id, to_id in arrows:
            self._draw_arrow(self.nodes[from_id], self.nodes[to_id])

    def _draw_arrow(self, start: FlowchartRect, end: FlowchartRect):
        start_point = start.center_bottom()
        end_point = end.center_top()
        pen = QPen(QColor("#c8a4ff"), 2)
        line = self.scene.addLine(start_point[0], start_point[1], end_point[0], end_point[1], pen)
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
        self.scene.addPolygon(polygon, pen, QColor("#c8a4ff"))

    def _node_clicked(self, node: FlowchartRect):
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
        self.slider.setRange(3, 200)
        self.slider.setValue(25)
        self.slider.valueChanged.connect(self.update_plot)
        layout.addWidget(QLabel("Adjust max list length (m/n) to see O(max(m,n)) growth:"))
        layout.addWidget(self.slider)

        self.update_plot(self.slider.value())

    def update_plot(self, n: int):
        self.ax.clear()
        x = list(range(1, n + 1))
        y = x
        self.ax.plot(x, y, color="#c8a4ff", label="Digits processed")
        self.ax.set_xlabel("max(len(l1), len(l2))")
        self.ax.set_ylabel("Relative work")
        self.ax.set_title("Time complexity O(max(m, n))")
        self.ax.grid(True, linestyle="--", alpha=0.4)
        self.ax.legend(loc="upper left")
        self.canvas.draw()


ADD_TWO_NUMS_TEMPLATE = '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def add_two_numbers(l1, l2):
    """Return the head of the new linked list sum."""
    carry = 0
    dummy = ListNode()
    cur = dummy

    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        carry = total // 10
        cur.next = ListNode(total % 10)
        cur = cur.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
'''


class CodeLabTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        description = QLabel(
            "Implement add_two_numbers(l1, l2) that accepts ListNode inputs (digits"
            " stored in reverse order). Syntax is checked live."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        self.editor = QPlainTextEdit()
        self.editor.setPlainText(ADD_TWO_NUMS_TEMPLATE)
        self.editor.setFont(QFont("JetBrains Mono", 11))
        PythonHighlighter(self.editor.document())
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

        self._syntax_error_line: int | None = None
        self.editor.textChanged.connect(self.lint_code)
        self.lint_code()

    def lint_code(self):
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

    def _highlight_error(self, line: int):
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

    def run_tests(self):
        if self._syntax_error_line is not None:
            self.feedback.setPlainText(
                f"Fix syntax error on line {self._syntax_error_line} before running tests."
            )
            return

        code = self.editor.toPlainText()
        namespace: Dict[str, object] = {"ListNode": ListNode}
        try:
            exec(code, namespace)
        except Exception as exc:  # noqa: BLE001
            self.feedback.setPlainText(f"Code error: {exc}\n{traceback.format_exc()}")
            return

        func = namespace.get("add_two_numbers")
        if not callable(func):
            self.feedback.setPlainText("Define add_two_numbers(l1, l2) in the editor above.")
            return

        cases = [
            ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
            ([0], [0], [0]),
            ([9, 9, 9, 9], [9, 9, 9, 9], [8, 9, 9, 9, 1]),
            ([5], [5], [0, 1]),
        ]

        for l1_list, l2_list, expected in cases:
            try:
                head = func(list_to_nodes(l1_list), list_to_nodes(l2_list))
            except Exception as exc:  # noqa: BLE001
                self.feedback.setPlainText(
                    f"Runtime error for {l1_list} + {l2_list}: {exc}\n{traceback.format_exc()}"
                )
                return

            answer = nodes_to_list(head)
            if answer != expected:
                self.feedback.setPlainText(
                    f"Wrong answer for {l1_list} + {l2_list}. Expected {expected}, got {answer}"
                )
                return

        self.feedback.setPlainText("All sample tests passed!")


class AddTwoNumbersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Two Numbers Learning Lab")
        tabs = QTabWidget()
        tabs.addTab(LessonTab(), "Lesson")
        tabs.addTab(PlaygroundTab(), "Playground")
        tabs.addTab(FlowchartTab(), "Flowchart")
        tabs.addTab(ComplexityTab(), "Complexity")
        tabs.addTab(CodeLabTab(), "Code Lab")
        self.setCentralWidget(tabs)
        self.resize(1024, 760)


def main():
    app = QApplication(sys.argv)
    set_futuristic_style(app)
    window = AddTwoNumbersWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
