from pathlib import Path
from typing import Tuple, Optional
import re


def load_lesson_markdown(file_path: Path) -> Tuple[bool, str]:
    """
    Load markdown content from a file.

    Args:
        file_path: Absolute or relative path to the markdown file.

    Returns:
        A tuple of (success, content) where success is True if file was loaded,
        and content is either the file contents or an error message.
    """
    if file_path.exists():
        try:
            content = file_path.read_text(encoding="utf-8")
            return True, content
        except Exception as e:
            return False, f"Error reading file: {e}"
    return False, f"Lesson file not found: {file_path}"


def markdown_to_html(md_content: str) -> str:
    """
    Convert markdown to HTML with basic formatting.
    This is a simple implementation - for full markdown support, use the 'markdown' library.
    """
    html = md_content

    # Escape HTML entities first
    html = html.replace('&', '&amp;')
    html = html.replace('<', '&lt;')
    html = html.replace('>', '&gt;')

    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Code blocks (triple backticks) - preserve newlines
    def format_code_block(match):
        lang = match.group(1)
        code = match.group(2)
        # Convert newlines to <br> for QTextBrowser
        code = code.replace('\n', '<br>')
        return f'<pre><code class="{lang}">{code}</code></pre>'

    html = re.sub(
        r'```(\w*)\n(.*?)```',
        format_code_block,
        html,
        flags=re.DOTALL
    )

    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Unordered lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n)+', r'<ul>\g<0></ul>', html)

    # Ordered lists
    html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Paragraphs (double newlines)
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = f'<p>{html}</p>'

    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    html = re.sub(r'<p>(<h[1-6]>)', r'\1', html)
    html = re.sub(r'(</h[1-6]>)</p>', r'\1', html)
    html = re.sub(r'<p>(<ul>)', r'\1', html)
    html = re.sub(r'(</ul>)</p>', r'\1', html)
    html = re.sub(r'<p>(<pre>)', r'\1', html)
    html = re.sub(r'(</pre>)</p>', r'\1', html)

    return html


def get_styled_html(content: str, is_dark: bool = True) -> str:
    """
    Wrap HTML content with styling for display in QTextBrowser.
    """
    bg_color = "#090d1a" if is_dark else "#ffffff"
    text_color = "#e5f4ff" if is_dark else "#1a1a1a"
    code_bg = "#1d1142" if is_dark else "#f0f0f0"
    heading_color = "#a678ff" if is_dark else "#6b46c1"
    link_color = "#00ffae" if is_dark else "#0066cc"
    border_color = "#462d7c" if is_dark else "#cccccc"

    return f"""
    <html>
    <head>
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: {heading_color};
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        h3 {{ font-size: 16px; }}
        code {{
            background-color: {code_bg};
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: {code_bg};
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid {border_color};
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        pre code {{
            background: none;
            padding: 0;
            white-space: pre-wrap;
        }}
        a {{
            color: {link_color};
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 5px;
        }}
        blockquote {{
            border-left: 4px solid {heading_color};
            padding-left: 16px;
            margin-left: 0;
            color: {text_color};
            opacity: 0.8;
        }}
        strong {{
            color: {heading_color};
        }}
    </style>
    </head>
    <body>
    {content}
    </body>
    </html>
    """


# Base directory for the application
def get_base_dir() -> Path:
    """Get the base directory of the pyqt6_learning_labs package."""
    return Path(__file__).resolve().parent.parent


def get_lessons_dir() -> Path:
    """Get the lessons directory (parent of pyqt6_learning_labs)."""
    return get_base_dir().parent
