"""
Safe code execution module with timeout and restricted builtins.
"""
import ast
import sys
from typing import Dict, Any, Tuple, Optional
from io import StringIO
import threading
import signal


# Dangerous modules that should not be imported
BLOCKED_MODULES = {
    'os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib',
    'requests', 'http', 'ftplib', 'smtplib', 'telnetlib',
    'pickle', 'shelve', 'marshal', 'importlib', 'builtins',
    '__builtins__', 'ctypes', 'multiprocessing', 'threading',
    'asyncio', 'concurrent', 'signal', 'resource', 'gc',
    'inspect', 'code', 'codeop', 'compile', 'exec', 'eval',
}

# Safe builtins for user code
SAFE_BUILTINS = {
    '__build_class__': __builtins__['__build_class__'] if isinstance(__builtins__, dict) else __builtins__.__build_class__,
    'abs': abs,
    'all': all,
    'any': any,
    'bin': bin,
    'bool': bool,
    'chr': chr,
    'dict': dict,
    'divmod': divmod,
    'enumerate': enumerate,
    'filter': filter,
    'float': float,
    'format': format,
    'frozenset': frozenset,
    'hash': hash,
    'hex': hex,
    'int': int,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'iter': iter,
    'len': len,
    'list': list,
    'map': map,
    'max': max,
    'min': min,
    'next': next,
    'oct': oct,
    'ord': ord,
    'pow': pow,
    'print': print,
    'range': range,
    'repr': repr,
    'reversed': reversed,
    'round': round,
    'set': set,
    'slice': slice,
    'sorted': sorted,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'type': type,
    'zip': zip,
    'True': True,
    'False': False,
    'None': None,
    'object': object,
    'property': property,
    'staticmethod': staticmethod,
    'classmethod': classmethod,
    'super': super,
}


class CodeSecurityError(Exception):
    """Raised when code contains potentially dangerous operations."""
    pass


class CodeTimeoutError(Exception):
    """Raised when code execution times out."""
    pass


class SafetyVisitor(ast.NodeVisitor):
    """AST visitor to check for dangerous code patterns."""

    def visit_Import(self, node):
        for alias in node.names:
            module_name = alias.name.split('.')[0]
            if module_name in BLOCKED_MODULES:
                raise CodeSecurityError(f"Import of '{module_name}' is not allowed")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            module_name = node.module.split('.')[0]
            if module_name in BLOCKED_MODULES:
                raise CodeSecurityError(f"Import from '{module_name}' is not allowed")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check for dangerous function calls
        if isinstance(node.func, ast.Name):
            if node.func.id in ('exec', 'eval', 'compile', '__import__', 'open'):
                raise CodeSecurityError(f"Call to '{node.func.id}' is not allowed")
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in ('system', 'popen', 'spawn', 'fork'):
                raise CodeSecurityError(f"Call to '{node.func.attr}' is not allowed")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Block access to dunder attributes
        if node.attr.startswith('__') and node.attr.endswith('__'):
            if node.attr not in ('__init__', '__str__', '__repr__', '__len__',
                                  '__iter__', '__next__', '__getitem__', '__setitem__',
                                  '__contains__', '__eq__', '__ne__', '__lt__', '__le__',
                                  '__gt__', '__ge__', '__hash__', '__bool__'):
                raise CodeSecurityError(f"Access to '{node.attr}' is not allowed")
        self.generic_visit(node)


def check_code_safety(code: str) -> None:
    """
    Check if code is safe to execute.
    Raises CodeSecurityError if dangerous patterns are found.
    """
    try:
        tree = ast.parse(code)
        SafetyVisitor().visit(tree)
    except SyntaxError as e:
        raise CodeSecurityError(f"Syntax error: {e}")


def execute_with_timeout(func, timeout: float = 5.0) -> Any:
    """
    Execute a function with a timeout.
    Note: This is a simple implementation - for production use consider
    using multiprocessing for true isolation.
    """
    result = [None]
    error = [None]

    def target():
        try:
            result[0] = func()
        except Exception as e:
            error[0] = e

    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise CodeTimeoutError(f"Code execution timed out after {timeout} seconds")

    if error[0]:
        raise error[0]

    return result[0]


def safe_exec(
    code: str,
    namespace: Optional[Dict[str, Any]] = None,
    timeout: float = 5.0
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Safely execute Python code with restrictions.

    Args:
        code: The Python code to execute
        namespace: Additional namespace variables to make available
        timeout: Maximum execution time in seconds

    Returns:
        Tuple of (success, message, namespace)
    """
    # First, check code safety
    try:
        check_code_safety(code)
    except CodeSecurityError as e:
        return False, f"Security Error: {e}", {}

    # Create restricted namespace
    exec_namespace: Dict[str, Any] = {
        '__builtins__': SAFE_BUILTINS,
        '__name__': '__main__',
    }

    # Add any additional namespace items
    if namespace:
        exec_namespace.update(namespace)

    # Capture stdout
    old_stdout = sys.stdout
    captured_output = StringIO()

    try:
        sys.stdout = captured_output

        def do_exec():
            exec(code, exec_namespace)

        execute_with_timeout(do_exec, timeout)

        output = captured_output.getvalue()
        return True, output if output else "Code executed successfully", exec_namespace

    except CodeTimeoutError as e:
        return False, str(e), {}
    except Exception as e:
        return False, f"Execution Error: {type(e).__name__}: {e}", {}
    finally:
        sys.stdout = old_stdout


def safe_exec_function(
    code: str,
    func_name: str,
    args: tuple = (),
    kwargs: Optional[Dict[str, Any]] = None,
    namespace: Optional[Dict[str, Any]] = None,
    timeout: float = 5.0
) -> Tuple[bool, Any, str]:
    """
    Safely execute code and call a specific function from it.

    Args:
        code: The Python code containing the function definition
        func_name: Name of the function to call
        args: Positional arguments for the function
        kwargs: Keyword arguments for the function
        namespace: Additional namespace variables
        timeout: Maximum execution time

    Returns:
        Tuple of (success, result, message)
    """
    if kwargs is None:
        kwargs = {}

    # First execute the code to define the function
    success, message, exec_namespace = safe_exec(code, namespace, timeout)

    if not success:
        return False, None, message

    # Check if the function exists
    if func_name not in exec_namespace:
        return False, None, f"Function '{func_name}' not found in code"

    func = exec_namespace[func_name]
    if not callable(func):
        return False, None, f"'{func_name}' is not callable"

    # Call the function with timeout
    try:
        def do_call():
            return func(*args, **kwargs)

        result = execute_with_timeout(do_call, timeout)
        return True, result, "Success"

    except CodeTimeoutError as e:
        return False, None, str(e)
    except Exception as e:
        return False, None, f"Error calling {func_name}: {type(e).__name__}: {e}"
