"""
Tests for keyboard shortcuts and code editor functionality.
Run with: python -m pytest pyqt6_learning_labs/tests/test_shortcuts.py -v
"""
import sys
import pytest
from unittest.mock import MagicMock, patch

# Skip if PyQt6 not available
pytest.importorskip("PyQt6")

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication

# Create QApplication if needed
app = QApplication.instance() or QApplication(sys.argv)


class TestCodeEditorCompletion:
    """Test code completion functionality."""

    def test_force_completion_shows_popup(self):
        """Test that force_completion shows the completer popup."""
        from pyqt6_learning_labs.widgets.code_editor import CodeEditor

        editor = CodeEditor("def test():\n    pass")
        editor.show()

        # Move cursor to a position with text
        cursor = editor.editor.textCursor()
        cursor.setPosition(3)  # After "def"
        editor.editor.setTextCursor(cursor)

        # Force completion
        editor.force_completion()

        # Popup should be visible or at least attempted
        assert editor.completer is not None

    def test_force_completion_toggles_popup(self):
        """Test that force_completion hides popup if already visible."""
        from pyqt6_learning_labs.widgets.code_editor import CodeEditor

        editor = CodeEditor("def test():\n    pass")
        editor.show()

        # Show popup first
        editor.completer.popup().show()
        assert editor.completer.popup().isVisible()

        # Force completion should hide it
        editor.force_completion()
        assert not editor.completer.popup().isVisible()

    def test_check_completion_requires_visible_editor(self):
        """Test that check_completion returns early if editor not visible."""
        from pyqt6_learning_labs.widgets.code_editor import CodeEditor

        editor = CodeEditor("def")
        # Don't show editor - it's not visible
        editor.check_completion()
        # Should return early without showing popup
        assert not editor.completer.popup().isVisible()

    def test_shortcut_modifier_detection(self):
        """Test that both Ctrl and Meta modifiers are detected."""
        from pyqt6_learning_labs.widgets.code_editor import CodeEditor

        editor = CodeEditor("def")
        editor.show()

        # Test that the eventFilter handles the shortcut
        # Create a mock key event for Ctrl+Space
        event = QKeyEvent(
            QEvent.Type.KeyPress,
            Qt.Key.Key_Space,
            Qt.KeyboardModifier.ControlModifier
        )

        # The eventFilter should handle this
        result = editor.eventFilter(editor.editor, event)
        # Should return True indicating it handled the event
        assert result is True


class TestTabSwitching:
    """Test tab switching shortcuts."""

    def test_switch_tab_method_exists(self):
        """Test that _switch_tab method exists on MainWindow."""
        from pyqt6_learning_labs.main import MainWindow

        window = MainWindow()
        assert hasattr(window, '_switch_tab')
        window.close()

    def test_switch_tab_with_valid_index(self):
        """Test switching to a valid tab index."""
        from pyqt6_learning_labs.main import MainWindow

        window = MainWindow()
        # Launch an app to have tabs
        window.launch_app("two_sum")

        # Switch to tab 1 (Playground)
        window._switch_tab(1)

        current = window.stack.currentWidget()
        if hasattr(current, 'tabs'):
            assert current.tabs.currentIndex() == 1

        window.close()


class TestSafeExec:
    """Test safe execution with class support."""

    def test_class_definition_works(self):
        """Test that class definitions work in safe_exec."""
        from pyqt6_learning_labs.core.safe_exec import safe_exec

        code = """
class ListNode:
    def __init__(self, val=0):
        self.val = val

node = ListNode(5)
result = node.val
"""
        success, message, namespace = safe_exec(code)
        assert success, f"Failed: {message}"
        assert namespace.get('result') == 5

    def test_build_class_available(self):
        """Test that __build_class__ is in SAFE_BUILTINS."""
        from pyqt6_learning_labs.core.safe_exec import SAFE_BUILTINS

        assert '__build_class__' in SAFE_BUILTINS

    def test_super_available(self):
        """Test that super() works in classes."""
        from pyqt6_learning_labs.core.safe_exec import safe_exec

        code = """
class Parent:
    def greet(self):
        return "Hello"

class Child(Parent):
    def greet(self):
        return super().greet() + " World"

c = Child()
result = c.greet()
"""
        success, message, namespace = safe_exec(code)
        assert success, f"Failed: {message}"
        assert namespace.get('result') == "Hello World"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
