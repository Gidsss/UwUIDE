import os
from pathlib import Path
import tempfile
import subprocess

from constants.path import BUILTIN_TYPES

class Compiler:
    def __init__(self, py_source: str, filename: str) -> None:
        if not (res := self.validate_file(filename)): return
        self.filename = res
        self.source = self.builtins() + py_source
        self.compile()
        self._run() # for testing purposes

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

    def _run(self):
        'for testing purposes only'
        exe_name = f"{self.filename}.exe"
        exe_path = Path("./dist") / exe_name
        subprocess.run([exe_path])

    def builtins(self) -> str:
        with open(BUILTIN_TYPES, 'r') as f:
            contents = f.read()
        return contents
