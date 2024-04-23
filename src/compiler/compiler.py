import os
from pathlib import Path
import tempfile
import subprocess

from constants.path import BUILTIN_TYPES

class Compiler:
    def __init__(self, py_source: str) -> None:
        self.source = self.builtins() + py_source
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.source)
            tmp_file_path = f.name
        subprocess.run(['pyinstaller', '--onefile', tmp_file_path, '--specpath', f'./build/{Path(tmp_file_path).stem}'])
        exe_name = f"{Path(tmp_file_path).stem}.exe"
        exe_path = Path("./dist") / exe_name
        subprocess.run([exe_path])
        os.remove(tmp_file_path)

    def builtins(self) -> str:
        with open(BUILTIN_TYPES, 'r') as f:
            contents = f.read()
        return contents
