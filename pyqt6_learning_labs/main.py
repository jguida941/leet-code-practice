import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QGraphicsOpacityEffect,
    QSizePolicy, QSizeGrip
)
from PyQt6.QtGui import QAction, QIcon, QFont, QColor, QPalette, QShortcut, QKeySequence, QCursor
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, QTimer, QRect

from pyqt6_learning_labs.core.theme import set_futuristic_style
from pyqt6_learning_labs.core.constants import Dimensions, Colors, Timing, Shortcuts
from pyqt6_learning_labs.apps.two_sum import TwoSumWidget
from pyqt6_learning_labs.apps.add_two_nums import AddTwoNumbersWidget


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 5, 15, 5)
        self.setFixedHeight(Dimensions.TITLE_BAR_HEIGHT)
        self.setStyleSheet(f"""
            CustomTitleBar {{
                background-color: {Colors.BG_MEDIUM};
                border: none;
                border-bottom: 2px solid {Colors.ACCENT_TERTIARY};
            }}
        """)

        self.title = QLabel("PyQt6 Learning Labs")
        self.title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: bold; font-size: 16px; background: transparent;")
        self.layout.addWidget(self.title)
        self.layout.addStretch()

        # Window Controls with better styling
        button_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_SECONDARY};
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
                border-radius: 15px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """

        self.btn_min = QPushButton("—")
        self.btn_min.setFixedSize(Dimensions.WINDOW_BUTTON_SIZE, Dimensions.WINDOW_BUTTON_SIZE)
        self.btn_min.clicked.connect(self.parent.showMinimized)
        self.btn_min.setStyleSheet(button_style + f"QPushButton:hover {{ color: {Colors.ACCENT_PRIMARY}; }}")
        self.btn_min.setAccessibleName("Minimize window")

        self.btn_max = QPushButton("◻")
        self.btn_max.setFixedSize(Dimensions.WINDOW_BUTTON_SIZE, Dimensions.WINDOW_BUTTON_SIZE)
        self.btn_max.clicked.connect(self.toggle_maximize)
        self.btn_max.setStyleSheet(button_style + f"QPushButton:hover {{ color: {Colors.ACCENT_SECONDARY}; }}")
        self.btn_max.setAccessibleName("Maximize window")

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(Dimensions.WINDOW_BUTTON_SIZE, Dimensions.WINDOW_BUTTON_SIZE)
        self.btn_close.clicked.connect(self.parent.close)
        self.btn_close.setStyleSheet(button_style + f"QPushButton:hover {{ color: {Colors.ERROR}; background-color: rgba(255, 85, 85, 0.2); }}")
        self.btn_close.setAccessibleName("Close window")

        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.start = QPoint(0, 0)
        self.pressing = False

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.btn_max.setText("◻")
        else:
            self.parent.showMaximized()
            self.btn_max.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start = self.mapToGlobal(event.pos())
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            # If maximized, restore first
            if self.parent.isMaximized():
                self.parent.showNormal()
                self.btn_max.setText("◻")
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.setGeometry(
                self.parent.x() + movement.x(),
                self.parent.y() + movement.y(),
                self.parent.width(),
                self.parent.height()
            )
            self.start = end

    def mouseReleaseEvent(self, event):
        self.pressing = False

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()


class AppCard(QFrame):
    def __init__(self, title, description, icon_text, on_click):
        super().__init__()
        self.setMinimumSize(Dimensions.CARD_WIDTH, Dimensions.CARD_HEIGHT)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.on_click = on_click
        self.is_hovered = False

        # Initial styling
        self.base_style = f"""
            AppCard {{
                background-color: {Colors.BG_CARD};
                border: 2px solid {Colors.BG_CARD_HOVER};
                border-radius: 12px;
            }}
        """
        self.hover_style = f"""
            AppCard {{
                background-color: {Colors.BG_CARD_HOVER};
                border: 2px solid {Colors.ACCENT_SECONDARY};
                border-radius: 12px;
            }}
        """
        self.setStyleSheet(self.base_style)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        # Icon with gradient background effect
        icon_container = QWidget()
        icon_container.setFixedSize(Dimensions.ICON_CONTAINER_SIZE, Dimensions.ICON_CONTAINER_SIZE)
        icon_container.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(0, 255, 174, 0.1);
                border-radius: {Dimensions.ICON_CONTAINER_SIZE // 2}px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel(icon_text)
        icon.setStyleSheet(f"font-size: 36px; color: {Colors.ACCENT_SECONDARY}; background: transparent; border: none; font-weight: bold;")
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
        lbl_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Colors.TEXT_PRIMARY}; background: transparent; border: none;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Description
        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet(f"font-size: 13px; color: {Colors.TEXT_SECONDARY}; background: transparent; border: none; line-height: 1.4;")
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_desc.setWordWrap(True)
        layout.addWidget(lbl_desc)

        layout.addStretch()

        # Accessibility
        self.setAccessibleName(title)
        self.setAccessibleDescription(description)

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
        title.setStyleSheet(f"font-size: 48px; font-weight: bold; color: {Colors.ACCENT_PRIMARY}; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(title)

        subtitle = QLabel("Master Algorithms with Interactive Visualizations")
        subtitle.setStyleSheet(f"font-size: 20px; color: {Colors.TEXT_PRIMARY}; opacity: 0.8;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(subtitle)

        # Keyboard hints
        hints = QLabel("Press Escape to return home anytime")
        hints.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_MUTED}; margin-top: 10px;")
        hints.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(hints)

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
            "Σ",
            lambda: on_launch("two_sum")
        )
        grid_layout.addWidget(card_two_sum)

        # Add Two Numbers Card
        card_add = AppCard(
            "Add Two Numbers",
            "Add two numbers represented by linked lists.",
            "+",
            lambda: on_launch("add_two_nums")
        )
        grid_layout.addWidget(card_add)

        layout.addWidget(grid_container)
        layout.addStretch()

        # Footer
        footer = QLabel("v2.0 • Premium Edition")
        footer.setStyleSheet(f"color: {Colors.ACCENT_TERTIARY}; font-size: 12px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)


class ResizableFramelessWindow(QMainWindow):
    """A frameless window that supports resizing from edges and corners."""

    def __init__(self):
        super().__init__()
        self._resize_margin = Dimensions.RESIZE_MARGIN
        self._resize_direction = None
        self._resize_start_pos = None
        self._resize_start_geometry = None
        self.setMouseTracking(True)

    def _get_resize_direction(self, pos):
        """Determine resize direction based on cursor position."""
        rect = self.rect()
        margin = self._resize_margin

        left = pos.x() < margin
        right = pos.x() > rect.width() - margin
        top = pos.y() < margin
        bottom = pos.y() > rect.height() - margin

        if left and top:
            return "top-left"
        elif right and top:
            return "top-right"
        elif left and bottom:
            return "bottom-left"
        elif right and bottom:
            return "bottom-right"
        elif left:
            return "left"
        elif right:
            return "right"
        elif top:
            return "top"
        elif bottom:
            return "bottom"
        return None

    def _update_cursor(self, direction):
        """Update cursor based on resize direction."""
        cursors = {
            "left": Qt.CursorShape.SizeHorCursor,
            "right": Qt.CursorShape.SizeHorCursor,
            "top": Qt.CursorShape.SizeVerCursor,
            "bottom": Qt.CursorShape.SizeVerCursor,
            "top-left": Qt.CursorShape.SizeFDiagCursor,
            "bottom-right": Qt.CursorShape.SizeFDiagCursor,
            "top-right": Qt.CursorShape.SizeBDiagCursor,
            "bottom-left": Qt.CursorShape.SizeBDiagCursor,
        }
        if direction:
            self.setCursor(cursors.get(direction, Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            direction = self._get_resize_direction(event.pos())
            if direction:
                self._resize_direction = direction
                self._resize_start_pos = event.globalPosition().toPoint()
                self._resize_start_geometry = self.geometry()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resize_direction and self._resize_start_pos:
            self._do_resize(event.globalPosition().toPoint())
        else:
            direction = self._get_resize_direction(event.pos())
            self._update_cursor(direction)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resize_direction = None
        self._resize_start_pos = None
        self._resize_start_geometry = None
        self._update_cursor(None)
        super().mouseReleaseEvent(event)

    def _do_resize(self, global_pos):
        """Perform the actual resize operation."""
        diff = global_pos - self._resize_start_pos
        geo = QRect(self._resize_start_geometry)
        min_w = Dimensions.MIN_WINDOW_WIDTH
        min_h = Dimensions.MIN_WINDOW_HEIGHT

        if "left" in self._resize_direction:
            new_left = geo.left() + diff.x()
            new_width = geo.width() - diff.x()
            if new_width >= min_w:
                geo.setLeft(new_left)

        if "right" in self._resize_direction:
            new_width = geo.width() + diff.x()
            if new_width >= min_w:
                geo.setWidth(new_width)

        if "top" in self._resize_direction:
            new_top = geo.top() + diff.y()
            new_height = geo.height() - diff.y()
            if new_height >= min_h:
                geo.setTop(new_top)

        if "bottom" in self._resize_direction:
            new_height = geo.height() + diff.y()
            if new_height >= min_h:
                geo.setHeight(new_height)

        self.setGeometry(geo)


class MainWindow(ResizableFramelessWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(Dimensions.DEFAULT_WINDOW_WIDTH, Dimensions.DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(Dimensions.MIN_WINDOW_WIDTH, Dimensions.MIN_WINDOW_HEIGHT)

        # Main Container with better border styling
        self.container = QWidget()
        self.container.setStyleSheet(f"""
            QWidget#main_container {{
                background-color: {Colors.BG_DARK};
                border: 2px solid {Colors.ACCENT_TERTIARY};
                border-radius: 12px;
            }}
        """)
        self.container.setObjectName("main_container")
        self.container.setMouseTracking(True)
        self.setCentralWidget(self.container)

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Custom Title Bar
        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        # Content Area
        self.content_area = QWidget()
        self.content_area.setMouseTracking(True)
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.addWidget(self.content_area)

        # Stacked Widget with opacity effect for transitions
        self.stack = QStackedWidget()
        self.stack.setMouseTracking(True)
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
        self.btn_home.setFixedSize(Dimensions.BUTTON_WIDTH, Dimensions.BUTTON_HEIGHT)
        self.btn_home.clicked.connect(self.go_home)
        self.btn_home.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_CARD};
                border: 2px solid {Colors.ACCENT_TERTIARY};
                border-radius: 6px;
                color: {Colors.TEXT_PRIMARY};
                font-weight: 600;
                padding: 4px 8px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_CARD_HOVER};
                border: 2px solid {Colors.ACCENT_SECONDARY};
                color: {Colors.ACCENT_SECONDARY};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_MEDIUM};
            }}
        """)
        self.btn_home.setAccessibleName("Return to home screen")
        self.btn_home.hide()
        self.title_bar.layout.insertWidget(1, self.btn_home)

        # Size grip for resizing (bottom-right corner)
        self.size_grip = QSizeGrip(self)
        self.size_grip.setStyleSheet("background: transparent;")

        # Setup keyboard shortcuts
        self._setup_shortcuts()

        # Animation for transitions
        self._setup_animations()

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts for navigation."""
        # Home shortcut
        home_shortcut = QShortcut(QKeySequence(Shortcuts.HOME), self)
        home_shortcut.activated.connect(self.go_home)

        # Escape to go home
        esc_shortcut = QShortcut(QKeySequence(Shortcuts.ESCAPE), self)
        esc_shortcut.activated.connect(self.go_home)

        # Run shortcut (Ctrl+R) - runs trace or tests depending on active tab
        run_shortcut = QShortcut(QKeySequence(Shortcuts.RUN), self)
        run_shortcut.activated.connect(self._on_run_shortcut)

        # Step forward (Ctrl+Right)
        forward_shortcut = QShortcut(QKeySequence(Shortcuts.STEP_FORWARD), self)
        forward_shortcut.activated.connect(self._on_step_forward)

        # Step back (Ctrl+Left)
        back_shortcut = QShortcut(QKeySequence(Shortcuts.STEP_BACK), self)
        back_shortcut.activated.connect(self._on_step_back)

    def _get_current_playground(self):
        """Get the playground widget from current app if available."""
        current = self.stack.currentWidget()
        if hasattr(current, 'playground'):
            return current.playground
        return None

    def _on_run_shortcut(self):
        """Handle Ctrl+R shortcut."""
        playground = self._get_current_playground()
        if playground and hasattr(playground, 'run_all'):
            playground.run_all()

    def _on_step_forward(self):
        """Handle Ctrl+Right shortcut."""
        playground = self._get_current_playground()
        if playground and hasattr(playground, 'step_forward'):
            playground.step_forward()

    def _on_step_back(self):
        """Handle Ctrl+Left shortcut."""
        playground = self._get_current_playground()
        if playground and hasattr(playground, 'step_back'):
            playground.step_back()

    def _setup_animations(self):
        """Setup fade animations for transitions."""
        self.fade_effect = QGraphicsOpacityEffect(self.stack)
        self.stack.setGraphicsEffect(self.fade_effect)
        self.fade_effect.setOpacity(1.0)

        self.fade_out_anim = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_out_anim.setDuration(Timing.FADE_DURATION_MS // 2)
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.fade_in_anim = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_in_anim.setDuration(Timing.FADE_DURATION_MS // 2)
        self.fade_in_anim.setStartValue(0.0)
        self.fade_in_anim.setEndValue(1.0)
        self.fade_in_anim.setEasingCurve(QEasingCurve.Type.InQuad)

        self._pending_widget = None

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
        if self.stack.currentWidget() != self.home:
            self.fade_transition(self.home)
            self.btn_home.hide()

    def fade_transition(self, target_widget):
        """Smooth fade out/in transition between widgets."""
        if self.stack.currentWidget() == target_widget:
            return

        self._pending_widget = target_widget

        # Disconnect previous connections to avoid multiple calls
        try:
            self.fade_out_anim.finished.disconnect()
        except TypeError:
            pass

        self.fade_out_anim.finished.connect(self._on_fade_out_complete)
        self.fade_out_anim.start()

    def _on_fade_out_complete(self):
        """Called when fade out is complete, switch widget and fade in."""
        if self._pending_widget:
            self.stack.setCurrentWidget(self._pending_widget)
            self._pending_widget = None
        self.fade_in_anim.start()

    def resizeEvent(self, event):
        """Position the size grip in the bottom-right corner."""
        super().resizeEvent(event)
        grip_size = 16
        self.size_grip.setGeometry(
            self.width() - grip_size - 4,
            self.height() - grip_size - 4,
            grip_size,
            grip_size
        )


def main():
    app = QApplication(sys.argv)
    set_futuristic_style(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
