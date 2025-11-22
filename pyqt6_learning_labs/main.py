import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QGraphicsOpacityEffect
from PyQt6.QtGui import QAction, QIcon, QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup

from pyqt6_learning_labs.core.theme import set_futuristic_style
from pyqt6_learning_labs.apps.two_sum import TwoSumWidget
from pyqt6_learning_labs.apps.add_two_nums import AddTwoNumbersWidget

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 5, 15, 5)
        self.setFixedHeight(45)
        self.setStyleSheet("""
            CustomTitleBar {
                background-color: #0f0a1f;
                border: none;
                border-bottom: 2px solid #462d7c;
            }
        """)

        self.title = QLabel("PyQt6 Learning Labs")
        self.title.setStyleSheet("color: #e5f4ff; font-weight: bold; font-size: 16px; background: transparent;")
        self.layout.addWidget(self.title)
        self.layout.addStretch()

        # Window Controls with better styling
        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #8b9bb4;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """

        self.btn_min = QPushButton("—")
        self.btn_min.setFixedSize(30, 30)
        self.btn_min.clicked.connect(self.parent.showMinimized)
        self.btn_min.setStyleSheet(button_style + "QPushButton:hover { color: #a678ff; }")

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.clicked.connect(self.parent.close)
        self.btn_close.setStyleSheet(button_style + "QPushButton:hover { color: #ff5555; background-color: rgba(255, 85, 85, 0.2); }")

        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.start = QPoint(0, 0)
        self.pressing = False

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.setGeometry(self.parent.x() + movement.x(), self.parent.y() + movement.y(), self.parent.width(), self.parent.height())
            self.start = end

    def mouseReleaseEvent(self, event):
        self.pressing = False

class AppCard(QFrame):
    def __init__(self, title, description, icon_text, on_click):
        super().__init__()
        self.setFixedSize(280, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.on_click = on_click
        self.is_hovered = False

        # Initial styling
        self.base_style = """
            AppCard {
                background-color: #1d1142;
                border: 2px solid #2d1b4e;
                border-radius: 12px;
            }
        """
        self.hover_style = """
            AppCard {
                background-color: #2d1b4e;
                border: 2px solid #00ffae;
                border-radius: 12px;
            }
        """
        self.setStyleSheet(self.base_style)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        # Icon with gradient background effect
        icon_container = QWidget()
        icon_container.setFixedSize(60, 60)
        icon_container.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 255, 174, 0.1);
                border-radius: 30px;
            }
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel(icon_text)
        icon.setStyleSheet("font-size: 36px; color: #00ffae; background: transparent; border: none; font-weight: bold;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon)

        # Center the icon container
        icon_wrapper = QWidget()
        icon_wrapper_layout = QHBoxLayout(icon_wrapper)
        icon_wrapper_layout.addStretch()
        icon_wrapper_layout.addWidget(icon_container)
        icon_wrapper_layout.addStretch()
        layout.addWidget(icon_wrapper)

        # Title
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #e5f4ff; background: transparent; border: none;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Description
        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet("font-size: 13px; color: #8b9bb4; background: transparent; border: none; line-height: 1.4;")
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_desc.setWordWrap(True)
        layout.addWidget(lbl_desc)

        layout.addStretch()

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.base_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()


class HomeWidget(QWidget):
    def __init__(self, on_launch):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(40)
        
        # Hero Section
        hero_layout = QVBoxLayout()
        title = QLabel("PyQt6 Learning Labs")
        title.setStyleSheet("font-size: 48px; font-weight: bold; color: #a678ff; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(title)
        
        subtitle = QLabel("Master Algorithms with Interactive Visualizations")
        subtitle.setStyleSheet("font-size: 20px; color: #e5f4ff; opacity: 0.8;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(subtitle)
        layout.addLayout(hero_layout)
        
        # Grid of Apps
        grid_container = QWidget()
        grid_layout = QHBoxLayout(grid_container)
        grid_layout.setSpacing(30)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Two Sum Card
        card_two_sum = AppCard(
            "Two Sum",
            "Find indices of two numbers that add up to a target.",
            "∑",
            lambda: on_launch("two_sum")
        )
        grid_layout.addWidget(card_two_sum)

        # Add Two Numbers Card
        card_add = AppCard(
            "Add Two Numbers",
            "Add two numbers represented by linked lists.",
            "⊕",
            lambda: on_launch("add_two_nums")
        )
        grid_layout.addWidget(card_add)
        
        layout.addWidget(grid_container)
        layout.addStretch()
        
        # Footer
        footer = QLabel("v2.0 • Premium Edition")
        footer.setStyleSheet("color: #462d7c; font-size: 12px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1200, 800)
        
        # Main Container with better border styling
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget#main_container {
                background-color: #090d1a;
                border: 2px solid #462d7c;
                border-radius: 12px;
            }
        """)
        self.container.setObjectName("main_container")
        self.setCentralWidget(self.container)
        
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Custom Title Bar
        self.title_bar = CustomTitleBar(self)
        self.layout.addWidget(self.title_bar)
        
        # Content Area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.content_area)
        
        # Stacked Widget
        self.stack = QStackedWidget()
        self.content_layout.addWidget(self.stack)
        
        # Home Screen
        self.home = HomeWidget(self.launch_app)
        self.stack.addWidget(self.home)
        
        # Apps
        self.two_sum_app = TwoSumWidget()
        self.add_two_nums_app = AddTwoNumbersWidget()
        
        self.stack.addWidget(self.two_sum_app)
        self.stack.addWidget(self.add_two_nums_app)
        
        # Home Button with better styling
        self.btn_home = QPushButton("← Home")
        self.btn_home.setFixedSize(80, 32)
        self.btn_home.clicked.connect(self.go_home)
        self.btn_home.setStyleSheet("""
            QPushButton {
                background-color: #1d1142;
                border: 2px solid #462d7c;
                border-radius: 6px;
                color: #e5f4ff;
                font-weight: 600;
                padding: 4px 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2d1b4e;
                border: 2px solid #00ffae;
                color: #00ffae;
            }
            QPushButton:pressed {
                background-color: #0f0a1f;
            }
        """)
        self.btn_home.hide()
        self.title_bar.layout.insertWidget(1, self.btn_home)

    def launch_app(self, app_name):
        target_widget = None
        if app_name == "two_sum":
            target_widget = self.two_sum_app
        elif app_name == "add_two_nums":
            target_widget = self.add_two_nums_app
            
        if target_widget:
            self.fade_transition(target_widget)
            self.btn_home.show()

    def go_home(self):
        self.fade_transition(self.home)
        self.btn_home.hide()

    def fade_transition(self, target_widget):
        # Simple fade out/in transition
        self.stack.setCurrentWidget(target_widget)
        
        # Note: Full animated transitions between widgets in QStackedWidget 
        # require more complex painting or QGraphicsView. 
        # For now, we just switch, but the buttons have hover effects.

def main():
    app = QApplication(sys.argv)
    set_futuristic_style(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
