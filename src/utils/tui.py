import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from utils.ansi import colorize


def _read_key_windows():
    """Ler uma tecla do teclado no Windows e mapear F1–F12, ESC, ENTER, dígitos e setas."""
    try:
        import msvcrt  # type: ignore
    except ImportError:
        return None

    ch = msvcrt.getch()
    # ENTER
    if ch in (b"\r", b"\n"):
        return "ENTER"
    # ESC
    if ch == b"\x1b":
        return "ESC"
    # Backspace
    if ch == b"\x08":
        return "BACKSPACE"
    # Dígitos e letras simples
    if ch.isalnum():
        try:
            return ch.decode().upper()
        except Exception:
            return None

    # Teclas estendidas: 0x00 ou 0xE0 precedem outra leitura
    if ch in (b"\x00", b"\xe0"):
        ch2 = msvcrt.getch()
        mapping = {
            b";": "F1", b"<": "F2", b"=": "F3", b">": "F4",
            b"?": "F5", b"@": "F6", b"A": "F7", b"B": "F8",
            b"C": "F9", b"D": "F10", b"\x85": "F11", b"\x86": "F12",
            b"H": "UP", b"P": "DOWN", b"K": "LEFT", b"M": "RIGHT",
            b"S": "DEL", b"G": "HOME", b"O": "END",
        }
        return mapping.get(ch2, None)
    return None


def read_key():
    """Ler uma tecla única de forma síncrona.
    No Windows, usa msvcrt. Em outros SOs, faz fallback para input() simples.
    Retorna um identificador de tecla como 'F1', 'ESC', 'ENTER', '1', 'A', etc.
    """
    if os.name == "nt":
        return _read_key_windows()
    # Fallback simples: ler uma linha e usar primeiro char
    try:
        text = input().strip()
        if not text:
            return None
        return text[0].upper()
    except EOFError:
        return None


def print_footer_hotkeys(hints, enabled_colors: bool = False, color: str | None = None):
    """Imprimir um rodapé com atalhos. hints: lista de tuplas (tecla, descrição)."""
    if not hints:
        return
    # Ex.: [ ("F1", "Pesquisar"), ("F2", "Nome"), ("F3", "Finalizar"), ... ]
    line = []
    for key, desc in hints:
        line.append(f"{key}:{desc}")
    footer = "  ".join(line)
    styled_footer = colorize(footer, color or "cyan", enabled_colors)
    print("\n" + "-" * max(60, len(footer)))
    print(styled_footer)
    print("-" * max(60, len(footer)))


def prompt_text(message: str) -> str:
    """Prompt simples preservando estilo de input padrão."""
    return input(message)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(usuario_nome: str | None, enabled_colors: bool = False, title_color: str | None = None):
    title = "           SISTEMA BANCAEXPERT - BANCA DE JORNAL"
    styled_title = colorize(title, title_color or "yellow", enabled_colors, bold=True)
    print("=" * 60)
    print(styled_title)
    print("=" * 60)
    if usuario_nome:
        print(f"Usuário: {usuario_nome} | Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print()


def print_title(text: str, enabled_colors: bool = False, color: str | None = None):
    print(colorize(f"\n{text}", color or "white", enabled_colors, bold=True))


def print_table(headers, rows, enabled_colors: bool = False, header_color: str | None = None, zebra: bool = True):
    """Imprime uma tabela simples com cabeçalho colorido e zebra opcional.
    headers: lista de (label, width)
    rows: lista de listas/tuplas com strings já formatadas
    """
    # Cabeçalho
    header_line = []
    for label, width in headers:
        header_line.append(f"{label:<{width}}")
    header_str = " ".join(header_line)
    print(header_str if not enabled_colors else colorize(header_str, header_color or "yellow", enabled_colors, bold=True))
    # Separador
    print("-" * len(header_str))
    # Linhas
    for idx, row in enumerate(rows):
        line_parts = []
        for (label, width), value in zip(headers, row):
            value_str = str(value)
            if len(value_str) > width:
                value_str = value_str[:width]
            line_parts.append(f"{value_str:<{width}}")
        line = " ".join(line_parts)
        if enabled_colors and zebra and (idx % 2 == 1):
            # Zebra com uma cor sutil
            print(colorize(line, "blue", True))
        else:
            print(line)


