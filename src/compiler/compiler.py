import os
from pathlib import Path
import tempfile
import subprocess

from constants.path import BUILTINS

class Compiler:
    def __init__(self, py_source: str, filename: str) -> None:
        if not (res := self.validate_file(filename)): return
        self.filename = res
        self.source = self.builtins() + py_source

    def validate_file(self, filename: str) -> str|None:
        # TODO: add more validations maybe?
        if not filename.endswith('.uwu'):
            print(f"File '{filename}' is not a .uwu file")
            return None
        return Path(filename).stem

    def compile(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.source)
            tmp_file_path = f.name
        subprocess.run(['pyinstaller',
                        '--name', f'{self.filename}.exe',
                        '--onefile', tmp_file_path,
                        '--specpath', f'./build/{self.filename}',
                        ])
        os.remove(tmp_file_path)

    def run(self):
        exe_name = f"{self.filename}.exe"
        exe_path = Path("./dist") / exe_name
        subprocess.run([exe_path])

    def run_python(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.source)
            tmp_file_path = f.name
        subprocess.run(['python', tmp_file_path])
        os.remove(tmp_file_path)

    def builtins(self) -> str:
        contents = "from __future__ import annotations\n\n"
        # remove any lines starting with
        remove = [
            "#",
            "from .namespace",
            "from __future__",
            "from src.",
        ]
        for path in BUILTINS:
            with open(path, 'r') as f:
                res = f.readlines()
                for r in remove:
                    res = [line for line in res if (
                        not line.strip().startswith(r)
                        and not line.strip() == '')
                    ]
                contents += ''.join(res) + '\n'
        return contents
