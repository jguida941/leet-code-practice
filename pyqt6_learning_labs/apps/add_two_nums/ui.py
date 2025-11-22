from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QGroupBox, QFormLayout, QLineEdit, QSpinBox, QPushButton, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from pyqt6_learning_labs.widgets.lesson import LessonWidget
from pyqt6_learning_labs.widgets.flowchart import FlowchartWidget
from pyqt6_learning_labs.widgets.complexity import ComplexityWidget
from pyqt6_learning_labs.widgets.code_editor import CodeEditor
from pyqt6_learning_labs.apps.add_two_nums.logic import add_two_numbers_logic, add_two_nums_complexity, list_to_nodes, nodes_to_list, ListNode
from pyqt6_learning_labs.apps.add_two_nums.config import FLOWCHART_NODES, FLOWCHART_EDGES, TEST_CASES, TEMPLATE_CODE

class AddTwoNumsPlayground(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Algorithm Trace")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #a678ff;")
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Enter digits for two linked lists (reverse order)."))
        
        # Inputs Section
        input_layout = QFormLayout()
        input_layout.setSpacing(15)
        
        self.list1_input = QLineEdit("2, 4, 3")
        self.list1_input.setPlaceholderText("e.g. 2, 4, 3")
        
        self.list2_input = QLineEdit("5, 6, 4")
        self.list2_input.setPlaceholderText("e.g. 5, 6, 4")
        
        self.base_spin = QSpinBox()
        self.base_spin.setRange(2, 10)
        self.base_spin.setValue(10)
        self.base_spin.setFixedWidth(100)
        
        lbl_l1 = QLabel("List A:")
        lbl_l1.setStyleSheet("font-weight: bold; color: #e5f4ff;")
        lbl_l2 = QLabel("List B:")
        lbl_l2.setStyleSheet("font-weight: bold; color: #e5f4ff;")
        lbl_base = QLabel("Base:")
        lbl_base.setStyleSheet("font-weight: bold; color: #e5f4ff;")
        
        input_layout.addRow(lbl_l1, self.list1_input)
        input_layout.addRow(lbl_l2, self.list2_input)
        input_layout.addRow(lbl_base, self.base_spin)
        layout.addLayout(input_layout)
        
        # Run Button
        run_btn = QPushButton("Add Numbers")
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
            l1 = [int(x.strip()) for x in self.list1_input.text().split(",") if x.strip()]
            l2 = [int(x.strip()) for x in self.list2_input.text().split(",") if x.strip()]
        except ValueError:
            self.result_label.setText("Error: Invalid input list")
            self.result_label.setStyleSheet("color: #ff5555; font-weight: bold; font-size: 16px;")
            return
            
        base = self.base_spin.value()
        result, trace = add_two_numbers_logic(l1, l2, base)
        
        self.result_label.setText(f"Result: {result}")
        self.result_label.setStyleSheet("color: #00ffae; font-weight: bold; font-size: 16px;")
        self.trace_box.setPlainText("\n".join(trace))


class AddTwoNumsCodeLab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Implement add_two_numbers(l1, l2)."))
        
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
        namespace = {"ListNode": ListNode}
        try:
            exec(code, namespace)
        except Exception as e:
            self.feedback.setPlainText(f"Error: {e}")
            return
            
        func = namespace.get("add_two_numbers")
        if not callable(func):
            self.feedback.setPlainText("Error: Function 'add_two_numbers' not found.")
            return
            
        results = []
        all_passed = True
        for l1_vals, l2_vals, expected in TEST_CASES:
            try:
                l1 = list_to_nodes(l1_vals)
                l2 = list_to_nodes(l2_vals)
                res_head = func(l1, l2)
                res = nodes_to_list(res_head)
                
                if res == expected:
                    results.append(f"PASS: {l1_vals} + {l2_vals} -> {res}")
                else:
                    results.append(f"FAIL: {l1_vals} + {l2_vals} -> Expected {expected}, Got {res}")
                    all_passed = False
            except Exception as e:
                results.append(f"ERROR: {l1_vals} + {l2_vals} -> {e}")
                all_passed = False
                
        final_msg = "\n".join(results)
        if all_passed:
            final_msg += "\n\nAll Tests Passed! Great Job!"
            
        self.feedback.setPlainText(final_msg)


class AddTwoNumbersWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        tabs = QTabWidget()
        
        # Lesson Tab - Check for lesson file and handle missing case
        lesson_path = Path(__file__).resolve().parents[4] / "add-two-numbers" / "lesson" / "add-two-nums.md"
        if not lesson_path.exists():
            # Fallback to a different possible location
            lesson_path = Path(__file__).resolve().parents[3] / "add-two-numbers" / "lesson" / "add-two-nums.md"
        tabs.addTab(LessonWidget(lesson_path, "Add Two Numbers Lesson"), "Lesson")
        
        # Playground Tab
        tabs.addTab(AddTwoNumsPlayground(), "Playground")
        
        # Flowchart Tab
        tabs.addTab(FlowchartWidget(FLOWCHART_NODES, FLOWCHART_EDGES), "Flowchart")
        
        # Complexity Tab
        tabs.addTab(ComplexityWidget("Time Complexity: O(max(m, n))", "Max List Length", "Operations", add_two_nums_complexity), "Complexity")
        
        # Code Lab Tab
        tabs.addTab(AddTwoNumsCodeLab(), "Code Lab")
        
        layout.addWidget(tabs)
