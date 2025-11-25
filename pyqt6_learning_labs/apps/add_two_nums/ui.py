from pathlib import Path
from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QTextEdit, QHBoxLayout,
    QProgressBar, QApplication
)
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from pyqt6_learning_labs.widgets.lesson import LessonWidget
from pyqt6_learning_labs.widgets.flowchart import FlowchartWidget
from pyqt6_learning_labs.widgets.complexity import ComplexityWidget
from pyqt6_learning_labs.widgets.code_editor import CodeEditor
from pyqt6_learning_labs.apps.add_two_nums.logic import (
    add_two_numbers_logic, add_two_nums_complexity,
    list_to_nodes, nodes_to_list, ListNode
)
from pyqt6_learning_labs.apps.add_two_nums.config import FLOWCHART_NODES, FLOWCHART_EDGES, TEST_CASES, TEMPLATE_CODE
from pyqt6_learning_labs.core.constants import Colors, Timing
from pyqt6_learning_labs.core.utils import get_lessons_dir
from pyqt6_learning_labs.core.safe_exec import safe_exec_function


class AddTwoNumsPlayground(QWidget):
    """Interactive playground with step-by-step execution and flowchart sync."""

    step_changed = pyqtSignal(str)

    def __init__(self, flowchart_widget: Optional[FlowchartWidget] = None):
        super().__init__()
        self.flowchart = flowchart_widget
        self.trace_steps: List[str] = []
        self.current_step = 0
        self.is_playing = False
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self._auto_step)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)

        # Top control bar - inputs and buttons together
        control_bar = QHBoxLayout()
        control_bar.setSpacing(12)

        # List A input
        lbl_l1 = QLabel("A:")
        lbl_l1.setStyleSheet(f"font-weight: bold; color: {Colors.TEXT_PRIMARY};")
        control_bar.addWidget(lbl_l1)

        self.list1_input = QLineEdit("2, 4, 3")
        self.list1_input.setPlaceholderText("e.g. 2, 4, 3")
        self.list1_input.setMinimumWidth(100)
        self.list1_input.setMaximumWidth(150)
        self.list1_input.textChanged.connect(self._on_input_changed)
        control_bar.addWidget(self.list1_input)

        # List B input
        lbl_l2 = QLabel("B:")
        lbl_l2.setStyleSheet(f"font-weight: bold; color: {Colors.TEXT_PRIMARY};")
        control_bar.addWidget(lbl_l2)

        self.list2_input = QLineEdit("5, 6, 4")
        self.list2_input.setPlaceholderText("e.g. 5, 6, 4")
        self.list2_input.setMinimumWidth(100)
        self.list2_input.setMaximumWidth(150)
        self.list2_input.textChanged.connect(self._on_input_changed)
        control_bar.addWidget(self.list2_input)

        # Base input
        lbl_base = QLabel("Base:")
        lbl_base.setStyleSheet(f"font-weight: bold; color: {Colors.TEXT_PRIMARY};")
        control_bar.addWidget(lbl_base)

        self.base_spin = QSpinBox()
        self.base_spin.setRange(2, 10)
        self.base_spin.setValue(10)
        self.base_spin.setMinimumWidth(60)
        self.base_spin.valueChanged.connect(self._on_input_changed)
        control_bar.addWidget(self.base_spin)

        control_bar.addSpacing(15)

        # Control buttons inline
        self.run_btn = QPushButton("▶ Run")
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_all)
        self.run_btn.setStyleSheet(f"background-color: {Colors.ACCENT_SECONDARY}; color: #000; font-weight: bold;")
        control_bar.addWidget(self.run_btn)

        self.step_back_btn = QPushButton("◀ Back")
        self.step_back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.step_back_btn.clicked.connect(self.step_back)
        self.step_back_btn.setEnabled(False)  # Disabled until we have steps to go back to
        control_bar.addWidget(self.step_back_btn)

        self.step_forward_btn = QPushButton("Next ▶")
        self.step_forward_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.step_forward_btn.clicked.connect(self.step_forward)
        control_bar.addWidget(self.step_forward_btn)

        self.play_btn = QPushButton("Auto")
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.clicked.connect(self.toggle_play)
        control_bar.addWidget(self.play_btn)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.reset)
        control_bar.addWidget(self.reset_btn)

        control_bar.addStretch()
        layout.addLayout(control_bar)

        # Status bar - progress + result on same line
        status_bar = QHBoxLayout()
        status_bar.setSpacing(15)

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFormat("Step %v of %m")
        self.progress.setFixedHeight(20)
        self.progress.setMinimumWidth(150)
        self.progress.setMaximumWidth(200)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Colors.BG_CARD};
                border: 1px solid {Colors.ACCENT_TERTIARY};
                border-radius: 3px;
                text-align: center;
                color: {Colors.TEXT_PRIMARY};
                font-size: 11px;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.ACCENT_SECONDARY};
                border-radius: 2px;
            }}
        """)
        status_bar.addWidget(self.progress)

        self.result_label = QLabel("Result: —")
        self.result_label.setStyleSheet(f"font-weight: bold; color: {Colors.ACCENT_SECONDARY};")
        status_bar.addWidget(self.result_label)

        status_bar.addStretch()

        self.export_btn = QPushButton("📋 Copy Trace")
        self.export_btn.clicked.connect(self.export_trace)
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.ACCENT_TERTIARY};
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_CARD};
                color: {Colors.ACCENT_SECONDARY};
            }}
        """)
        status_bar.addWidget(self.export_btn)
        layout.addLayout(status_bar)

        # Current step display
        self.current_step_label = QLabel("Click ▶ Run to execute the algorithm")
        self.current_step_label.setStyleSheet(f"""
            font-size: 13px;
            color: {Colors.TEXT_PRIMARY};
            background-color: {Colors.BG_CARD};
            padding: 10px 12px;
            border-radius: 4px;
            border-left: 3px solid {Colors.ACCENT_PRIMARY};
        """)
        self.current_step_label.setWordWrap(True)
        layout.addWidget(self.current_step_label)

        # Trace output - takes remaining space
        self.trace_box = QTextEdit()
        self.trace_box.setReadOnly(True)
        self.trace_box.setPlaceholderText("Execution trace will appear here...")
        self.trace_box.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_CARD};
                border: 1px solid {Colors.ACCENT_TERTIARY};
                border-radius: 4px;
                padding: 12px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.5;
            }}
        """)
        layout.addWidget(self.trace_box, 1)

        # Map trace patterns to flowchart nodes
        self._node_patterns = {
            "Input A:": "start",
            "Input B:": "start",
            "Base:": "start",
            "v1=": "read",
            "total=": "sum",
            "write digit": "split",
            "carry out": "append",
            "Result digits": "done",
        }

    def _get_flowchart_node(self, step_text: str) -> Optional[str]:
        """Determine which flowchart node corresponds to a trace step."""
        for pattern, node_key in self._node_patterns.items():
            if pattern in step_text:
                return node_key
        return None

    def _update_flowchart(self, step_text: str):
        """Update flowchart highlighting based on current step."""
        if self.flowchart:
            node_key = self._get_flowchart_node(step_text)
            if node_key:
                self.flowchart.highlight_node(node_key)
                self.step_changed.emit(node_key)

    def run_all(self):
        """Run the complete trace at once."""
        try:
            l1 = [int(x.strip()) for x in self.list1_input.text().split(",") if x.strip()]
            l2 = [int(x.strip()) for x in self.list2_input.text().split(",") if x.strip()]
        except ValueError:
            self.result_label.setText("Error: Invalid input list")
            self.result_label.setStyleSheet(f"color: {Colors.ERROR}; font-weight: bold;")
            return

        base = self.base_spin.value()
        result, self.trace_steps = add_two_numbers_logic(l1, l2, base)

        self.result_label.setText(f"Result: {result}")
        self.result_label.setStyleSheet(f"color: {Colors.ACCENT_SECONDARY}; font-weight: bold;")

        # Show all steps at once
        self.current_step = len(self.trace_steps)
        self.trace_box.setPlainText("\n".join(self.trace_steps))
        self.progress.setMaximum(len(self.trace_steps))
        self.progress.setValue(len(self.trace_steps))

        if self.trace_steps:
            self.current_step_label.setText(self.trace_steps[-1])
            self._update_flowchart(self.trace_steps[-1])

        self._update_buttons()

    def step_forward(self):
        """Advance one step in the trace."""
        if not self.trace_steps:
            try:
                l1 = [int(x.strip()) for x in self.list1_input.text().split(",") if x.strip()]
                l2 = [int(x.strip()) for x in self.list2_input.text().split(",") if x.strip()]
            except ValueError:
                self.result_label.setText("Error: Invalid input list")
                return

            base = self.base_spin.value()
            result, self.trace_steps = add_two_numbers_logic(l1, l2, base)
            self.current_step = 0
            self.progress.setMaximum(len(self.trace_steps))

            self.result_label.setText(f"Result: {result}")
            self.result_label.setStyleSheet(f"color: {Colors.ACCENT_SECONDARY}; font-weight: bold;")

        if self.current_step < len(self.trace_steps):
            step_text = self.trace_steps[self.current_step]
            self.current_step += 1
            self.progress.setValue(self.current_step)
            self.current_step_label.setText(step_text)
            self._update_flowchart(step_text)
            self.trace_box.setPlainText("\n".join(self.trace_steps[:self.current_step]))

        self._update_buttons()

    def step_back(self):
        """Go back one step in the trace."""
        if self.current_step > 1:
            self.current_step -= 1
            self.progress.setValue(self.current_step)
            step_text = self.trace_steps[self.current_step - 1]
            self.current_step_label.setText(step_text)
            self._update_flowchart(step_text)
            self.trace_box.setPlainText("\n".join(self.trace_steps[:self.current_step]))
        elif self.current_step == 1:
            self.current_step = 0
            self.progress.setValue(0)
            self.current_step_label.setText("Click ▶ Run to execute the algorithm")
            self.trace_box.clear()

        self._update_buttons()

    def toggle_play(self):
        """Toggle auto-play mode."""
        if self.is_playing:
            self.is_playing = False
            self.play_timer.stop()
            self.play_btn.setText("Auto")
        else:
            if not self.trace_steps:
                self.step_forward()
            self.is_playing = True
            self.play_btn.setText("⏸ Pause")
            self.play_timer.start(Timing.STEP_DELAY_MS)

    def _auto_step(self):
        """Called by timer for auto-play."""
        if self.current_step < len(self.trace_steps):
            self.step_forward()
        else:
            self.toggle_play()

    def _on_input_changed(self):
        """Reset trace when inputs change since old trace is invalid."""
        if self.trace_steps:  # Only reset if there's an existing trace
            self.reset()

    def reset(self):
        """Reset the playground state."""
        self.is_playing = False
        self.play_timer.stop()
        self.play_btn.setText("Auto")
        self.trace_steps = []
        self.current_step = 0
        self.progress.setValue(0)
        self.progress.setMaximum(100)
        self.result_label.setText("Result: —")
        self.result_label.setStyleSheet(f"font-weight: bold; color: {Colors.ACCENT_SECONDARY};")
        self.current_step_label.setText("Click ▶ Run to execute the algorithm")
        self.trace_box.clear()
        self._update_buttons()

    def _update_buttons(self):
        """Update button states based on current state."""
        has_trace = len(self.trace_steps) > 0
        at_start = self.current_step == 0
        at_end = has_trace and self.current_step >= len(self.trace_steps)

        # Back only enabled if we have steps to go back to
        self.step_back_btn.setEnabled(has_trace and not at_start)
        # Forward enabled unless we're at the end of a completed trace
        self.step_forward_btn.setEnabled(not at_end)
        # Auto enabled unless we're at the end of a completed trace
        self.play_btn.setEnabled(not at_end)

    def export_trace(self):
        """Copy trace to clipboard."""
        if self.trace_steps:
            clipboard = QApplication.clipboard()
            trace_text = f"Add Two Numbers Trace\n{'='*40}\n"
            trace_text += f"List A: {self.list1_input.text()}\n"
            trace_text += f"List B: {self.list2_input.text()}\n"
            trace_text += f"Base: {self.base_spin.value()}\n"
            trace_text += f"{'='*40}\n\n"
            trace_text += "\n".join(self.trace_steps)
            trace_text += f"\n\n{self.result_label.text()}"
            clipboard.setText(trace_text)

            original_text = self.export_btn.text()
            self.export_btn.setText("Copied!")
            QTimer.singleShot(1500, lambda: self.export_btn.setText(original_text))


class AddTwoNumsCodeLab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Instructions
        header = QLabel("Code Lab - Implement add_two_numbers(l1, l2)")
        header.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {Colors.ACCENT_PRIMARY};")
        layout.addWidget(header)

        instructions = QLabel(
            "Write your implementation below. The function receives two linked lists "
            "representing numbers in reverse order and should return a new linked list with the sum."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(instructions)

        self.editor = CodeEditor(TEMPLATE_CODE)
        layout.addWidget(self.editor)

        # Button row
        btn_layout = QHBoxLayout()

        test_btn = QPushButton("Run Tests")
        test_btn.clicked.connect(self.run_tests)
        test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        test_btn.setAccessibleName("Run test cases against your code")
        btn_layout.addWidget(test_btn)

        reset_btn = QPushButton("Reset Code")
        reset_btn.clicked.connect(self.reset_code)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.ACCENT_TERTIARY};
            }}
            QPushButton:hover {{
                color: {Colors.ERROR};
                border-color: {Colors.ERROR};
            }}
        """)
        btn_layout.addWidget(reset_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Results
        self.feedback = QTextEdit()
        self.feedback.setReadOnly(True)
        self.feedback.setMaximumHeight(180)
        self.feedback.setPlaceholderText("Test results will appear here...")
        layout.addWidget(self.feedback)

    def reset_code(self):
        """Reset code to template."""
        self.editor.set_code(TEMPLATE_CODE)
        self.feedback.clear()

    def run_tests(self):
        code = self.editor.get_code()

        results = []
        all_passed = True
        tests_run = 0

        for l1_vals, l2_vals, expected in TEST_CASES:
            # Create linked lists for safe execution namespace
            namespace = {"ListNode": ListNode}

            # First compile the code to define add_two_numbers
            success, result, message = safe_exec_function(
                code,
                "add_two_numbers",
                args=(list_to_nodes(l1_vals), list_to_nodes(l2_vals)),
                namespace=namespace,
                timeout=2.0
            )

            tests_run += 1

            if not success:
                results.append(f"ERROR: {l1_vals} + {l2_vals} -> {message}")
                all_passed = False
            else:
                res = nodes_to_list(result)
                if res == expected:
                    results.append(f"PASS: {l1_vals} + {l2_vals} -> {res}")
                else:
                    results.append(f"FAIL: {l1_vals} + {l2_vals} -> Expected {expected}, Got {res}")
                    all_passed = False

        final_msg = "\n".join(results)
        if all_passed and tests_run > 0:
            final_msg += f"\n\nAll {tests_run} Tests Passed! Great Job!"
            self.feedback.setStyleSheet(f"color: {Colors.SUCCESS};")
        else:
            self.feedback.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        self.feedback.setPlainText(final_msg)


class AddTwoNumbersWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        tabs = QTabWidget()

        # Lesson Tab
        lesson_path = get_lessons_dir() / "add-two-numbers" / "lesson" / "add-two-nums.md"
        tabs.addTab(LessonWidget(lesson_path, "Add Two Numbers Lesson"), "Lesson")

        # Create flowchart first so we can pass it to playground
        self.flowchart = FlowchartWidget(FLOWCHART_NODES, FLOWCHART_EDGES)

        # Playground Tab with flowchart sync
        self.playground = AddTwoNumsPlayground(self.flowchart)
        tabs.addTab(self.playground, "Playground")

        # Flowchart Tab
        tabs.addTab(self.flowchart, "Flowchart")

        # Complexity Tab
        tabs.addTab(
            ComplexityWidget(
                "Time Complexity: O(max(m, n))",
                "Max List Length",
                "Operations",
                add_two_nums_complexity
            ),
            "Complexity"
        )

        # Code Lab Tab
        tabs.addTab(AddTwoNumsCodeLab(), "Code Lab")

        layout.addWidget(tabs)

        # Setup tab shortcuts
        for i in range(min(5, tabs.count())):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
            shortcut.activated.connect(lambda idx=i: tabs.setCurrentIndex(idx))
