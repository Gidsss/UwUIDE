from pathlib import Path

ROOT = Path(__file__).parent.parent

RUN_ASSET = Path('./assets/run.png')
LOAD_ASSET = Path('./assets/import.png')
SAVE_ASSET = Path('./assets/save.png')
FORMAT_ASSET = Path('./assets/load.png')
LOGO_WHITE_ASSET = Path('./assets/logo_white.png')
LOGO_BLACK_ASSET = Path('./assets/logo_black.png')
AQUACL_BG_ASSET = Path('./assets/aquaConsoleBG.png')
AQUACE_BG_ASSET = Path('./assets/aquacated.png')
WELCOME_BG_ASSET = Path('./assets/welcome_bg.png')
ICON_WHITE_ASSET = Path('./assets/icon_white.ico')
ICON_BLACK_ASSET = Path('./assets/icon_black.ico')

BUILTIN_TYPES = [
    ROOT / 'src' / 'builtin' / 'types' / 'namespace.py',
    ROOT / 'src' / 'builtin' / 'types' / 'iterable.py',
    ROOT / 'src' / 'builtin' / 'types' / 'number.py',
]
