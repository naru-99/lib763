import re
from typing import Dict, Pattern

# 数字に一致するパターン
PATTERN_DIGIT = r"\d"
# 英大文字に一致するパターン
PATTERN_UPPERCASE = r"[A-Z]"
# 英小文字に一致するパターン
PATTERN_LOWERCASE = r"[a-z]"
# 英字に一致するパターン
PATTERN_ALPHABET = r"[A-Za-z]"
# アルファベットまたは数字に一致するパターン
PATTERN_ALPHANUMERIC = r"[A-Za-z0-9]"
# スペースに一致するパターン
PATTERN_WHITESPACE = r"\s"
# メールアドレスに一致するパターン
PATTERN_EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def replace_pattern(input_string: str, pattern: Pattern, replacement: str) -> str:
    """指定したパターンを特定の文字列に置換する関数

    Args:
        input_string (str): 入力文字列。
        pattern (Pattern): 置換されるべきパターン。
        replacement (str): 置換する文字列。

    Returns:
        str: パターンが置換された文字列。
    """
    return re.sub(pattern, replacement, input_string)


def replace_patterns(input_string: str, replacements: Dict[Pattern, str]) -> str:
    """複数のパターンを対応する文字列に置換する関数

    Args:
        input_string (str): 入力文字列。
        replacements (Dict[Pattern, str]): キーがパターンで値が置換する文字列の辞書。

    Returns:
        str: パターンが置換された文字列。
    """
    for pattern, replacement in replacements.items():
        input_string = replace_pattern(input_string, pattern, replacement)
    return input_string
