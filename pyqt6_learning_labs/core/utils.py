from pathlib import Path

def load_lesson_markdown(file_path: Path) -> str:
    """
    Load markdown content from a file.
    
    Args:
        file_path: Absolute or relative path to the markdown file.
        
    Returns:
        The content of the file or an error message if not found.
    """
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return f"Lesson file missing: {file_path}"
