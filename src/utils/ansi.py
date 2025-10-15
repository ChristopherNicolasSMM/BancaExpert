# Suporte simples a cores ANSI

ANSI_CODES = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}


def colorize(text: str, color: str | None, enabled: bool, bold: bool = False) -> str:
    if not enabled:
        return text
    start_color = ANSI_CODES.get(color.lower(), "") if color else ""
    start_bold = ANSI_CODES.get("bold", "") if bold else ""
    start = f"{start_bold}{start_color}"
    if not start:
        return text
    end = ANSI_CODES["reset"]
    return f"{start}{text}{end}"


