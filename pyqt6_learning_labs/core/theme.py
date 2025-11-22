from PyQt6.QtWidgets import QApplication

def set_futuristic_style(app: QApplication) -> None:
    """Apply a consistent, clean dark theme."""
    app.setStyleSheet(
        """
        /* Global Widget Settings */
        QWidget {
            background-color: #090d1a;
            color: #e5f4ff;
            font-family: 'Arial', 'Segoe UI', 'SF Pro Display', sans-serif;
            font-size: 14px;
        }

        /* Labels */
        QLabel {
            color: #e5f4ff;
            background-color: transparent;
            border: none;
        }

        /* Main Window */
        QMainWindow {
            background-color: #090d1a;
        }

        /* Buttons */
        QPushButton {
            background-color: #1d1142;
            color: #e5f4ff;
            border: 2px solid #462d7c;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: #2d1b4e;
            border: 2px solid #00ffae;
            color: #00ffae;
        }
        QPushButton:pressed {
            background-color: #0f0a1f;
            border: 2px solid #00ffae;
        }

        /* Line Edits and Text Areas */
        QLineEdit, QPlainTextEdit, QTextEdit, QTextBrowser {
            background-color: #0f0a1f;
            color: #e5f4ff;
            border: 2px solid #2d1b4e;
            border-radius: 6px;
            padding: 8px;
            selection-background-color: #462d7c;
            selection-color: #ffffff;
        }
        QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus {
            border: 2px solid #a678ff;
            outline: none;
        }

        /* Spin Box */
        QSpinBox {
            background-color: #0f0a1f;
            color: #e5f4ff;
            border: 2px solid #2d1b4e;
            border-radius: 6px;
            padding: 6px;
            selection-background-color: #462d7c;
        }
        QSpinBox:focus {
            border: 2px solid #a678ff;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #1d1142;
            border: 1px solid #2d1b4e;
            width: 20px;
        }
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #2d1b4e;
        }
        QSpinBox::up-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-bottom: 4px solid #00ffae;
            width: 0;
            height: 0;
        }
        QSpinBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #00ffae;
            width: 0;
            height: 0;
        }

        /* Group Box */
        QGroupBox {
            background-color: transparent;
            border: 2px solid #2d1b4e;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
            font-size: 14px;
        }
        QGroupBox::title {
            color: #a678ff;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            padding: 0 8px;
            background-color: #090d1a;
        }

        /* Tab Widget */
        QTabWidget::pane {
            background-color: transparent;
            border: none;
            margin-top: -1px;
        }
        QTabBar::tab {
            background-color: transparent;
            color: #8b9bb4;
            padding: 12px 24px;
            margin-right: 4px;
            border: none;
            border-bottom: 3px solid transparent;
            font-weight: 600;
            font-size: 14px;
        }
        QTabBar::tab:selected {
            color: #00ffae;
            border-bottom: 3px solid #00ffae;
            background-color: transparent;
        }
        QTabBar::tab:hover:!selected {
            color: #e5f4ff;
            background-color: rgba(70, 45, 124, 0.2);
        }

        /* Frames */
        QFrame {
            background-color: transparent;
        }

        /* Sliders */
        QSlider::groove:horizontal {
            background-color: #1d1142;
            height: 8px;
            border-radius: 4px;
            border: 1px solid #2d1b4e;
        }
        QSlider::handle:horizontal {
            background-color: #00ffae;
            border: 2px solid #00ffae;
            width: 20px;
            height: 20px;
            margin: -7px 0;
            border-radius: 10px;
        }
        QSlider::handle:horizontal:hover {
            background-color: #00ffdd;
            border: 2px solid #00ffdd;
        }

        /* Scrollbars */
        QScrollBar:vertical {
            background-color: #0f0a1f;
            width: 12px;
            border: none;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #2d1b4e;
            min-height: 30px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #462d7c;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
            background: none;
        }
        QScrollBar:horizontal {
            background-color: #0f0a1f;
            height: 12px;
            border: none;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal {
            background-color: #2d1b4e;
            min-width: 30px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #462d7c;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
            background: none;
        }

        /* Tool Tips */
        QToolTip {
            background-color: #1d1142;
            color: #e5f4ff;
            border: 1px solid #462d7c;
            padding: 4px;
            border-radius: 4px;
        }
    """
    )
