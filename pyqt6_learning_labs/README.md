# PyQt6 Learning Labs

An interactive algorithm learning platform built with PyQt6. Master data structures and algorithms through step-by-step visualizations, interactive playgrounds, and hands-on coding challenges.

## Features

### Core Features

- **Step-by-Step Execution** - Walk through algorithms one step at a time with visual feedback
- **Flowchart Visualization** - Interactive flowcharts that sync with algorithm execution
- **Code Lab** - Write and test your own implementations with instant feedback
- **Complexity Analysis** - Visual graphs showing time/space complexity
- **Lesson Content** - Markdown-rendered educational content for each problem

### UI/UX Features

- **Dark Theme** - Beautiful dark purple/cyan color scheme optimized for focus
- **Custom Frameless Window** - Draggable title bar with minimize, maximize, close buttons
- **Resizable Window** - Resize from any edge or corner
- **Smooth Transitions** - Fade animations between screens
- **Keyboard Shortcuts** - Navigate quickly with keyboard
- **Progress Indicators** - Track your progress through algorithm steps

### Educational Features

- **Auto-Play Mode** - Watch the algorithm execute automatically
- **Trace Export** - Copy execution traces to clipboard for notes
- **Copy Code** - One-click copy of code implementations
- **Extended Test Cases** - Comprehensive test suites including edge cases
- **Syntax Highlighting** - Python code highlighting in the editor
- **Real-time Linting** - Instant syntax error feedback

## Keyboard Shortcuts

**Navigation**
- `Escape` - Return to home screen
- `Ctrl+1` through `Ctrl+5` - Switch between tabs

**Playground Controls**
- `Ctrl+R` - Run trace (or run tests in Code Lab)
- `Ctrl+Right` - Step forward in trace
- `Ctrl+Left` - Step back in trace

**Code Editor**
- `Ctrl+Space` - Trigger code completion

## Project Structure

```
pyqt6_learning_labs/
├── main.py                 # Application entry point
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── core/                   # Core utilities and configuration
│   ├── __init__.py
│   ├── constants.py        # Colors, dimensions, timing, shortcuts
│   ├── theme.py            # Global stylesheet and theming
│   ├── utils.py            # Markdown parsing, path utilities
│   └── safe_exec.py        # Sandboxed code execution
├── widgets/                # Reusable UI components
│   ├── __init__.py
│   ├── code_editor.py      # Syntax-highlighted code editor
│   ├── complexity.py       # Complexity visualization widget
│   ├── flowchart.py        # Interactive flowchart widget
│   └── lesson.py           # Markdown lesson viewer
└── apps/                   # Problem-specific implementations
    ├── two_sum/
    │   ├── __init__.py
    │   ├── ui.py           # Two Sum UI with playground & code lab
    │   ├── logic.py        # Algorithm implementation with trace
    │   └── config.py       # Flowchart nodes, test cases, template
    └── add_two_nums/
        ├── __init__.py
        ├── ui.py           # Add Two Numbers UI
        ├── logic.py        # Algorithm implementation
        └── config.py       # Configuration and test cases
```

## Core Modules

### `core/constants.py`

Centralized configuration for:
- `Dimensions` - Window sizes, button sizes, margins
- `Colors` - Theme colors (backgrounds, accents, text, syntax)
- `Timing` - Animation durations, debounce delays
- `Shortcuts` - Keyboard shortcut definitions

### `core/theme.py`

Global Qt stylesheet providing consistent styling for:
- Buttons, inputs, text areas
- Tab widgets, sliders, scrollbars
- Group boxes, tooltips

### `core/safe_exec.py`

Sandboxed Python code execution with:
- AST-based security checking
- Blocked dangerous imports (os, sys, subprocess, etc.)
- Execution timeout protection
- Safe builtin whitelist

### `core/utils.py`

Utility functions:
- Markdown to HTML conversion
- Styled HTML generation
- Base directory resolution

## Widget Components

### `CodeEditor`

Full-featured code editor with:
- Python syntax highlighting (keywords, strings, comments, numbers)
- Line numbers
- Current line highlighting
- Syntax error detection and highlighting
- Auto-completion for Python keywords
- Debounced linting (300ms)
- Copy to clipboard button

### `FlowchartWidget`

Interactive algorithm flowchart:
- Zoomable and pannable canvas
- Clickable nodes with detail view
- Node highlighting for step sync
- Arrow connections between nodes

### `ComplexityWidget`

Complexity visualization:
- Dynamic plotting (uses pyqtgraph if available, fallback otherwise)
- Adjustable input size slider
- Clear axis labels

### `LessonWidget`

Markdown content viewer:
- HTML rendering with styling
- Syntax highlighting for code blocks
- Reload button for live editing

## Adding a New Problem

1. Create a new directory under `apps/`:
```
apps/new_problem/
├── __init__.py
├── ui.py
├── logic.py
└── config.py
```

2. Define in `config.py`:
```python
FLOWCHART_NODES = {
    "start": ("Title", "Description", x, y),
    # ... more nodes
}

FLOWCHART_EDGES = [
    ("start", "next_node"),
    # ... connections
]

TEST_CASES = [
    (input1, input2, expected_output),
    # ... more cases
]

TEMPLATE_CODE = '''def solution(...):
    pass
'''
```

3. Implement in `logic.py`:
```python
def problem_logic(input) -> Tuple[result, List[str]]:
    trace = []
    # ... algorithm with trace.append() calls
    return result, trace
```

4. Create UI in `ui.py` following the pattern from `two_sum/ui.py`

5. Register in `main.py`:
```python
from pyqt6_learning_labs.apps.new_problem import NewProblemWidget
# Add to HomeWidget cards and MainWindow
```

## Running the Application

```bash
# From the repository root
python launch_learning_labs.py

# Or directly
python -m pyqt6_learning_labs.main
```

## Dependencies

- `PyQt6>=6.4.0` - Qt6 bindings for Python
- `pyqtgraph>=0.13.3` (optional) - Better complexity graphs

Install with:
```bash
pip install -r pyqt6_learning_labs/requirements.txt
```

## Security Notes

The Code Lab feature executes user-provided Python code. The `safe_exec` module provides several layers of protection:

1. **AST Validation** - Checks for dangerous patterns before execution
2. **Import Blocking** - Prevents importing dangerous modules
3. **Timeout Protection** - Limits execution time to prevent infinite loops
4. **Restricted Builtins** - Only safe built-in functions are available

However, this is not a complete sandbox. For production use, consider:
- Running in a container/VM
- Using a proper sandbox like `RestrictedPython`
- Limiting resource usage with `resource` module

## Version History

- **v2.1** - Added step-by-step execution, flowchart sync, safe exec, more test cases
- **v2.0** - Major UI overhaul with dark theme, custom window chrome
- **v1.0** - Initial release with basic Two Sum and Add Two Numbers

## License

MIT License - Feel free to use for learning and teaching!
