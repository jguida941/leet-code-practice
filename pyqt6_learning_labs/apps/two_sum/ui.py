from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QGroupBox, QFormLayout, QLineEdit, QSpinBox, QPushButton, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from pyqt6_learning_labs.widgets.lesson import LessonWidget
from pyqt6_learning_labs.widgets.flowchart import FlowchartWidget
from pyqt6_learning_labs.widgets.complexity import ComplexityWidget
from pyqt6_learning_labs.widgets.code_editor import CodeEditor
from pyqt6_learning_labs.apps.two_sum.logic import two_sum_logic, two_sum_complexity
from pyqt6_learning_labs.apps.two_sum.config import FLOWCHART_NODES, FLOWCHART_EDGES, TEST_CASES, TEMPLATE_CODE

class TwoSumPlayground(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Algorithm Trace")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #a678ff;")
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Enter numbers and target to see the step-by-step execution."))
        
        # Inputs Section
        input_layout = QFormLayout()
        input_layout.setSpacing(15)
        
        self.list_input = QLineEdit("2, 7, 11, 15")
        self.list_input.setPlaceholderText("e.g. 2, 7, 11, 15")
        
        self.target_input = QSpinBox()
        self.target_input.setRange(-1000000, 1000000)
        self.target_input.setValue(9)
        self.target_input.setFixedWidth(150)
        
        lbl_nums = QLabel("Numbers:")
        lbl_nums.setStyleSheet("font-weight: bold; color: #e5f4ff;")
        lbl_target = QLabel("Target:")
        lbl_target.setStyleSheet("font-weight: bold; color: #e5f4ff;")
        
        input_layout.addRow(lbl_nums, self.list_input)
        input_layout.addRow(lbl_target, self.target_input)
        layout.addLayout(input_layout)
        
        # Run Button
        run_btn = QPushButton("Run Trace")
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.clicked.connect(self.run)
        layout.addWidget(run_btn)
        
        # Results Section
        layout.addSpacing(20)
        self.result_label = QLabel("Result: ?")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #00ffae;")
        layout.addWidget(self.result_label)
        
        self.trace_box = QTextEdit()
        self.trace_box.setReadOnly(True)
        self.trace_box.setPlaceholderText("Execution trace will appear here...")
        layout.addWidget(self.trace_box)

    def run(self):
        try:
            nums = [int(x.strip()) for x in self.list_input.text().split(",") if x.strip()]
        except ValueError:
            self.result_label.setText("Error: Invalid input list")
            self.result_label.setStyleSheet("color: #ff5555; font-weight: bold; font-size: 16px;")
            return
            
        target = self.target_input.value()
        indices, trace = two_sum_logic(nums, target)
        
        if indices:
            self.result_label.setText(f"Result: Found at indices {indices}")
            self.result_label.setStyleSheet("color: #00ffae; font-weight: bold; font-size: 16px;")
        else:
            self.result_label.setText("Result: No pair found")
            self.result_label.setStyleSheet("color: #ff5555; font-weight: bold; font-size: 16px;")
            
        self.trace_box.setPlainText("\n".join(trace))


class TwoSumCodeLab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Implement two_sum(nums, target)."))
        
        self.editor = CodeEditor(TEMPLATE_CODE)
        layout.addWidget(self.editor)
        
        test_btn = QPushButton("Run Tests")
        test_btn.clicked.connect(self.run_tests)
        layout.addWidget(test_btn)
        
        self.feedback = QTextEdit()
        self.feedback.setReadOnly(True)
        self.feedback.setMaximumHeight(150)
        layout.addWidget(self.feedback)

    def run_tests(self):
        code = self.editor.get_code()
        namespace = {}
        try:
            exec(code, namespace)
        except Exception as e:
            self.feedback.setPlainText(f"Error: {e}")
            return
            
        func = namespace.get("two_sum")
        if not callable(func):
            self.feedback.setPlainText("Error: Function 'two_sum' not found.")
            return
            
        results = []
        all_passed = True
        for nums, target, expected in TEST_CASES:
            try:
                # Pass a copy of nums to avoid mutation side effects
                res = func(list(nums), target)
                if res == expected:
                    results.append(f"PASS: {nums}, {target} -> {res}")
                else:
                    results.append(f"FAIL: {nums}, {target} -> Expected {expected}, Got {res}")
                    all_passed = False
            except Exception as e:
                results.append(f"ERROR: {nums}, {target} -> {e}")
                all_passed = False
                
        final_msg = "\n".join(results)
        if all_passed:
            final_msg += "\n\nAll Tests Passed! Great Job!"
            
        self.feedback.setPlainText(final_msg)


class TwoSumWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        tabs = QTabWidget()
        
        # Lesson Tab - Check for lesson file and handle missing case
        lesson_path = Path(__file__).resolve().parents[4] / "two-sum" / "python" / "lesson" / "two-sum-lesson.md"
        if not lesson_path.exists():
            # Fallback to a different possible location
            lesson_path = Path(__file__).resolve().parents[3] / "two-sum" / "python" / "lesson" / "two-sum-lesson.md"
        tabs.addTab(LessonWidget(lesson_path, "Two Sum Lesson"), "Lesson")
        
        # Playground Tab
        tabs.addTab(TwoSumPlayground(), "Playground")
        
        # Flowchart Tab
        tabs.addTab(FlowchartWidget(FLOWCHART_NODES, FLOWCHART_EDGES), "Flowchart")
        
        # Complexity Tab
        tabs.addTab(ComplexityWidget("Time Complexity: O(n)", "Input Size (n)", "Operations", two_sum_complexity), "Complexity")
        
        # Code Lab Tab
        tabs.addTab(TwoSumCodeLab(), "Code Lab")
        
        layout.addWidget(tabs)
