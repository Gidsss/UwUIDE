from pathlib import Path

ROOT = Path(__file__).parent.parent

NEW_TAB_ASSET = ROOT / "assets" / "new_tab.png"
RUN_ASSET = ROOT / "assets" / "run.png"
QUICK_RUN_ASSET = ROOT / "assets" / "quick_run.png"
LOAD_ASSET = ROOT / "assets" / "import.png"
SAVE_ASSET = ROOT / "assets" / "save.png"
FORMAT_ASSET = ROOT / "assets" / "load.png"
LOGO_WHITE_ASSET = ROOT / "assets" / "logo_white.png"
LOGO_BLACK_ASSET = ROOT / "assets" / "logo_black.png"
AQUACL_BG_ASSET = ROOT / "assets" / "aquaConsoleBG.png"
AQUACE_BG_ASSET = ROOT / "assets" / "aquacated.png"
WELCOME_BG_ASSET = ROOT / "assets" / "welcome_bg.png"
ICON_WHITE_ASSET = ROOT / "assets" / "icon_white.png"
ICON_BLACK_ASSET = ROOT / "assets" / "icon_black.png"

BUILTIN_TYPES = [
    ROOT / "src" / "builtin" / "types" / "namespace.py",
    ROOT / "src" / "builtin" / "types" / "iterable.py",
    ROOT / "src" / "builtin" / "types" / "number.py",
]
BUILTINS = [
    *BUILTIN_TYPES,
    ROOT / "src" / "builtin" / "random" / "random.py",
]

LEXER_SOURCE = ROOT / "files" / "package-lexer.uwu"
PARSER_SOURCE = ROOT / "files" / "package-parser.uwu"
ANALYZER_SOURCE = ROOT / "files" / "package-analyzer.uwu"
COMPILE_SOURCE = ROOT / "files" / "package-compile.uwu"
