import math
from typing import Dict, List, Tuple, Callable, Optional
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QPen, QFont, QPainter, QPolygonF, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QPushButton

class FlowchartNode(QGraphicsRectItem):
    WIDTH = 240
    HEIGHT = 90
    
    def __init__(
        self,
        key: str,
        title: str,
        detail: str,
        x: int,
        y: int,
        scene: QGraphicsScene,
        on_click: Callable[["FlowchartNode"], None],
    ) -> None:
        super().__init__(x, y, self.WIDTH, self.HEIGHT)
        self.key = key
        self.title = title
        self.detail = detail
        self.on_click = on_click
        self.is_selected = False
        
        # Title text
        self.text_item = scene.addText(title)
        self.text_item.setDefaultTextColor(QColor("#e5f4ff"))
        self.text_item.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        self.text_item.setPos(x + 15, y + 15)
        self.text_item.setZValue(1)
        
        scene.addItem(self)
        self.setZValue(0)
        self.x_pos = x
        self.y_pos = y

    def paint(self, painter: QPainter, option, widget=None):
        # Custom paint for rounded corners and gradients
        rect = self.rect()
        
        # Gradient Background
        if self.is_selected:
            gradient = QColor("#00c2a8")
            border_color = QColor("#00ffae")
            border_width = 2
        else:
            gradient = QColor("#1b2735")
            border_color = QColor("#462d7c")
            border_width = 1

        painter.setBrush(gradient)
        painter.setPen(QPen(border_color, border_width))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawRoundedRect(rect, 10, 10)

    def set_selected(self, selected: bool) -> None:
        self.is_selected = selected
        self.update()

    def center_bottom(self) -> Tuple[float, float]:
        return (self.x_pos + self.WIDTH / 2, self.y_pos + self.HEIGHT)

    def center_top(self) -> Tuple[float, float]:
        return (self.x_pos + self.WIDTH / 2, self.y_pos)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self)
        super().mousePressEvent(event)


class FlowchartWidget(QWidget):
    """
    A generic flowchart widget that renders nodes and edges with interactive Zoom and Pan.
    """
    def __init__(self, nodes_data: Dict[str, Tuple[str, str, int, int]], edges: List[Tuple[str, str]]):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 10, 10, 0)
        toolbar_layout.setSpacing(8)
        
        self.info_label = QLabel("Scroll/Drag to Navigate • Click for Details")
        self.info_label.setStyleSheet("color: #8b9bb4; font-size: 12px;")
        toolbar_layout.addWidget(self.info_label)
        toolbar_layout.addStretch()
        
        # Zoom Controls with consistent styling
        button_style = """
            QPushButton {
                background-color: #1d1142;
                color: #e5f4ff;
                border: 2px solid #462d7c;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2d1b4e;
                border: 2px solid #00ffae;
                color: #00ffae;
            }
            QPushButton:pressed {
                background-color: #0f0a1f;
            }
        """

        btn_zoom_in = QPushButton("+")
        btn_zoom_in.setFixedSize(40, 34)
        btn_zoom_in.clicked.connect(lambda: self.zoom(1.2))
        btn_zoom_in.setStyleSheet(button_style)
        toolbar_layout.addWidget(btn_zoom_in)

        btn_zoom_out = QPushButton("−")
        btn_zoom_out.setFixedSize(40, 34)
        btn_zoom_out.clicked.connect(lambda: self.zoom(1/1.2))
        btn_zoom_out.setStyleSheet(button_style)
        toolbar_layout.addWidget(btn_zoom_out)

        btn_reset = QPushButton("Reset")
        btn_reset.setMinimumWidth(80)
        btn_reset.setFixedHeight(34)
        btn_reset.clicked.connect(self.reset_view)
        btn_reset.setStyleSheet(button_style + """
            QPushButton {
                padding: 0 12px;
            }
        """)
        toolbar_layout.addWidget(btn_reset)
        
        layout.addLayout(toolbar_layout)

        # Graphics View
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor("#070c1a"))
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        layout.addWidget(self.view, stretch=1)

        # Detail Box
        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)
        self.detail_box.setMinimumHeight(100)
        self.detail_box.setPlaceholderText("Select a step to see details...")
        self.detail_box.setStyleSheet("border-top: 1px solid #2d1b4e;")
        layout.addWidget(self.detail_box)

        self.nodes: Dict[str, FlowchartNode] = {}
        self.selected_node: Optional[FlowchartNode] = None
        
        self._build_graph(nodes_data, edges)

    def _build_graph(self, nodes_data, edges):
        # Create Nodes
        for key, (title, detail, x, y) in nodes_data.items():
            node = FlowchartNode(key, title, detail, x, y, self.scene, self._on_node_click)
            self.nodes[key] = node

        # Create Edges
        for from_key, to_key in edges:
            if from_key in self.nodes and to_key in self.nodes:
                self._draw_arrow(self.nodes[from_key], self.nodes[to_key])

    def _draw_arrow(self, start: FlowchartNode, end: FlowchartNode):
        start_point = start.center_bottom()
        end_point = end.center_top()
        
        pen = QPen(QColor("#462d7c"), 2)
        line = self.scene.addLine(
            start_point[0], start_point[1], end_point[0], end_point[1], pen
        )
        line.setZValue(-1)

        # Arrowhead
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
        
        self.scene.addPolygon(polygon, QPen(QColor("#462d7c")), QColor("#462d7c"))

    def _on_node_click(self, node: FlowchartNode):
        if self.selected_node:
            self.selected_node.set_selected(False)
        
        node.set_selected(True)
        self.selected_node = node
        self.detail_box.setPlainText(node.detail)

    def highlight_node(self, key: str):
        """Programmatically highlight a node (e.g. from trace execution)."""
        if key in self.nodes:
            self._on_node_click(self.nodes[key])
            self.view.ensureVisible(self.nodes[key])

    def reset_view(self):
        self.view.resetTransform()
        self.view.centerOn(0, 0) # Approximate center

    def zoom(self, factor):
        self.view.scale(factor, factor)

    def wheelEvent(self, event):
        """Zoom in/out with mouse wheel (No Ctrl required)."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        # Check delta for standard mouse or trackpad
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom(zoom_in_factor)
        elif delta < 0:
            self.zoom(zoom_out_factor)
        event.accept()
