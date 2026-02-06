import csv
import io
import re
from typing import List


def clean_text(text: str) -> str:
    """Clean and sanitize a log message."""
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text.strip())
    # Remove null bytes
    text = text.replace("\x00", "")
    # Limit length
    if len(text) > 5000:
        text = text[:5000]
    return text


def parse_csv_logs(csv_content: str) -> List[str]:
    """Parse CSV content and extract log messages."""
    logs = []
    reader = csv.reader(io.StringIO(csv_content))
    for row in reader:
        if row:
            # Join all columns as a single log message
            message = " | ".join(col.strip() for col in row if col.strip())
            if message:
                logs.append(clean_text(message))
    return logs


def parse_text_logs(text_content: str) -> List[str]:
    """Parse plain text logs (one per line)."""
    logs = []
    for line in text_content.strip().split("\n"):
        cleaned = clean_text(line)
        if cleaned:
            logs.append(cleaned)
    return logs


def validate_file_content(content: str, max_size: int = 1_000_000) -> bool:
    """Validate file content size and basic structure."""
    if len(content) > max_size:
        return False
    if not content.strip():
        return False
    return True


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection."""
    # Remove potential script tags
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()
