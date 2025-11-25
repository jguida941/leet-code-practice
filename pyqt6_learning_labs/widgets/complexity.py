from typing import Callable, List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QFrame
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QFont

from pyqt6_learning_labs.core.constants import Colors

try:
    import pyqtgraph as pg
    HAS_PYQTGRAPH = True
except ImportError:
    HAS_PYQTGRAPH = False

class SimplePlotWidget(QFrame):
    """Simple plot widget fallback when pyqtgraph is not available"""
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(300)
        self.setStyleSheet("background-color: #090d1a; border: 1px solid #2d1b4e; border-radius: 6px;")
        self.x_data = []
        self.y_data = []
        self.title = ""
        self.x_label = ""
        self.y_label = ""

    def setTitle(self, title):
        self.title = title

    def setLabels(self, x_label, y_label):
        self.x_label = x_label
        self.y_label = y_label

    def setData(self, x, y):
        self.x_data = x
        self.y_data = y
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw axes
        pen = QPen(QColor("#462d7c"), 2)
        painter.setPen(pen)

        rect = self.rect()
        margin = 50
        plot_rect = QRect(margin, margin, rect.width() - 2*margin, rect.height() - 2*margin)

        # Draw border
        painter.drawRect(plot_rect)

        # Draw title
        painter.setPen(QColor("#e5f4ff"))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter, self.title)

        # Draw grid and plot
        if self.x_data and self.y_data:
            pen = QPen(QColor("#00ffae"), 3)
            painter.setPen(pen)

            # Simple line plot
            max_x = max(self.x_data) if self.x_data else 1
            max_y = max(self.y_data) if self.y_data else 1

            points = []
            for x, y in zip(self.x_data, self.y_data):
                px = plot_rect.left() + (x / max_x) * plot_rect.width()
                py = plot_rect.bottom() - (y / max_y) * plot_rect.height()
                points.append((px, py))

            # Draw lines between points
            for i in range(len(points) - 1):
                painter.drawLine(int(points[i][0]), int(points[i][1]),
                               int(points[i+1][0]), int(points[i+1][1]))

class ComplexityWidget(QWidget):
    """
    A widget to visualize time complexity using PyQtGraph or fallback.
    """
    def __init__(self, title: str, x_label: str, y_label: str, complexity_func: Callable[[int], List[int]]):
        super().__init__()
        self.complexity_func = complexity_func

        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #a678ff; padding: 10px;")
        layout.addWidget(title_label)

        if HAS_PYQTGRAPH:
            # Use PyQtGraph if available
            self.plot_widget = pg.PlotWidget()
            self.plot_widget.setBackground("#090d1a")
            self.plot_widget.setTitle(title, color="#e5f4ff", size="12pt")
            self.plot_widget.setLabel("left", y_label, color="#e5f4ff")
            self.plot_widget.setLabel("bottom", x_label, color="#e5f4ff")
            self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
            self.pen = pg.mkPen(color="#00ffae", width=3)
        else:
            # Use fallback plot widget
            self.plot_widget = SimplePlotWidget()
            self.plot_widget.setTitle(title)
            self.plot_widget.setLabels(x_label, y_label)
            self.pen = None

        layout.addWidget(self.plot_widget)

        # Slider
        slider_label = QLabel("Adjust input size:")
        slider_label.setStyleSheet("color: #e5f4ff; margin-top: 10px;")
        layout.addWidget(slider_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(5, 200)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.update_plot)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #1d1142;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00ffae;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #00ffdd;
            }
        """)
        layout.addWidget(self.slider)

        # Initial plot
        self.update_plot(self.slider.value())

    def update_plot(self, n: int):
        x = list(range(1, n + 1))
        y = self.complexity_func(n)

        if HAS_PYQTGRAPH:
            self.plot_widget.clear()
            self.plot_widget.plot(x, y, pen=self.pen)
        else:
            self.plot_widget.setData(x, y)
