# couldyou_chatbot/telegram_bot/utils.py
import re
from typing import List
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def escape_markdown_v2(text: str) -> str:
    """Escape special characters for MarkdownV2"""
    if not text:
        return ""

    # Print original text
        logger.debug(f"Original text: {text}")

    # Characters that need to be escaped in MarkdownV2
    special_chars = ['[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

    # escape_char = r"_~`>#+-=|{}.!()[]"
    # First escape backslashes
    text = text.replace('\\', '')
    logger.debug(f"After escaping backslashes: {text}")

    # Then escape all other special characters
    for char in special_chars:
        text = text.replace(char, f'\{char}')

    # Print final escaped text
    # logger.debug(f"Final escaped text: {text}")
    print(f"Final escaped text: {text}\n")

    return text

def format_text_with_style(text: str, style: str = None) -> str:
    """Apply consistent styling to text with proper escaping"""
    escaped_text = escape_markdown_v2(text.strip())
    if style == "bold":
        return f"*{escaped_text}*"  # Changed from ** to *
    elif style == "italic":
        return f"_{escaped_text}_"
    elif style == "bold_italic":
        return f"*_{escaped_text}_*"
    elif style == "underline":
        return f"__{escaped_text}__"
    elif style == "strikethrough":
        return f"~{escaped_text}~"
    elif style == "code":
        return f"`{escaped_text}`"
    elif style == "pre":
        return f"```{escaped_text}```"
    return escaped_text

def create_formatted_response(text: str) -> List[str]:
    """Create beautifully formatted response chunks with consistent styling"""
    sections = text.split('\n\n')
    formatted_sections = []

    for section in sections:
        if re.match(r'(?i)^(step|how to|guide):', section):
            formatted_sections.append(format_instructions(section))
        elif re.match(r'(?i)^(warning|caution|important):', section):
            formatted_sections.append(format_warning(section))
        elif re.match(r'(?i)^(tip|note):', section):
            formatted_sections.append(format_tip(section))
        elif re.match(r'(?i)^(q:|question:)', section):
            formatted_sections.append(format_qa(section))
        else:
            formatted_sections.append(format_general_content(section))

    # Join sections with decorative dividers
    text = '\n\n━━━━━━━━━━━━━━━━━━━━━\n\n'.join(formatted_sections)
    chunks = split_into_chunks(text)
    return decorate_chunks(chunks)

def format_instructions(section: str) -> str:
    """Format instruction sections with consistent styling"""
    lines = section.split('\n')
    title = lines[0].strip().rstrip(':')
    steps = lines[1:] if len(lines) > 1 else []

    # Format header with consistent styling
    header = f"📝 {format_text_with_style(title, 'bold')}\n\n"

    formatted_steps = []
    for i, step in enumerate(steps, 1):
        if step.strip():
            # Format step number in bold and step text normally
            step_text = format_text_with_style(step.strip())
            formatted_steps.append(f"* {i}\\.* {step_text}")

    return header + '\n'.join(formatted_steps)

def format_warning(section: str) -> str:
    """Format warning sections with consistent styling"""
    lines = section.split('\n')
    title = lines[0].strip().rstrip(':')
    content = '\n'.join(lines[1:]) if len(lines) > 1 else ""

    warning_header = f"⚠️ {format_text_with_style(title, 'bold')}"
    warning_content = format_text_with_style(content)

    return f"{warning_header}\n\n{warning_content}"

def format_tip(section: str) -> str:
    """Format tips with consistent styling"""
    lines = section.split('\n')
    title = lines[0].strip().rstrip(':')
    content = '\n'.join(lines[1:]) if len(lines) > 1 else ""

    tip_header = f"💡 {format_text_with_style(title, 'bold')}"
    tip_content = format_text_with_style(content)

    return f"{tip_header}\n\n{tip_content}"

def format_qa(section: str) -> str:
    """Format Q&A sections with consistent styling"""
    try:
        q, a = section.split('\n', 1)
        question = format_text_with_style(q.replace('Q:', '').strip(), 'bold')
        answer = format_text_with_style(a.strip())
        return f"❓ {question}\n\n💬 {answer}"
    except ValueError:
        return f"❓ {format_text_with_style(section.strip())}"

def format_general_content(section: str) -> str:
    """Format general content with consistent styling"""
    lines = section.split('\n')
    formatted_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Format numbered points
        if re.match(r'^\d+\.', line):
            num, text = line.split('.', 1)
            formatted_lines.append(f"*{num}\\.* {format_text_with_style(text)}")

        # Format bullet points
        elif line.startswith(('- ', '* ')):
            text = format_text_with_style(line[2:])
            formatted_lines.append(f"• {text}")

        # Format headers (lines ending with :)
        elif line.endswith(':'):
            formatted_lines.append(format_text_with_style(line, 'bold'))

        # Format key terms and statistics
        else:
            formatted_line = format_text_with_style(line)
            # Bold numbers and statistics
            formatted_line = re.sub(
                r'(\d+(?:\.\d+)?(?:\s*%)?)(?=[^\d]|$)',
                r'*\1*',
                formatted_line
            )
            formatted_lines.append(formatted_line)

    return '\n'.join(formatted_lines)

def decorate_chunks(chunks: List[str]) -> List[str]:
    """Add consistently styled headers and footers to chunks"""
    if not chunks:
        return [format_text_with_style("No content available", "italic")]

    decorated = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            # First chunk gets styled header
            chunk = (
                f"🌸 {format_text_with_style('CouldYou? Cup Assistant', 'bold')}\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{chunk}"
            )

        if i == len(chunks) - 1:
            # Last chunk gets styled footer
            chunk = (
                f"{chunk}\n\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"{format_text_with_style('Feel free to ask more questions!', 'italic')}\n"
                f"{format_text_with_style('Use /start to return to main menu', 'italic')}\n"
                f"{format_text_with_style('Visit our website for more information', 'italic')}"
            )

        decorated.append(chunk)

    return decorated

def split_into_chunks(text: str, max_length: int = 4096) -> List[str]:
    """Split text into chunks while preserving formatting"""
    if not text:
        return [format_text_with_style("No content available", "italic")]

    chunks = []
    current_chunk = ""

    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 2 <= max_length:
            current_chunk += f"{line}\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = f"{line}\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def format_api_response(text: str) -> str:
    """Format API response with proper Markdown V2 styling"""
    # Format headers
    text = re.sub(r'^(#+)\s*(.+)$', r'*\2*', text, flags=re.MULTILINE)

    # Format lists
    text = re.sub(r'^\s*[-*]\s+(.+)$', r'• \1', text, flags=re.MULTILINE)

    # Format numbered lists
    text = re.sub(r'^\s*(\d+)\.\s+(.+)$', r'*\1\.* \2', text, flags=re.MULTILINE)

    # Format code blocks
    text = re.sub(r'```(.+?)```', r'`\1`', text, flags=re.DOTALL)

    # Format inline code
    text = re.sub(r'`([^`]+)`', r'`\1`', text)

    # Format bold
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)

    # Format italic
    text = re.sub(r'_(.+?)_', r'_\1_', text)

    # Format links
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'[\1](\2)', text)

    return escape_markdown_v2(text)
