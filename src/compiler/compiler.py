import os
from pathlib import Path
import tempfile
import subprocess
import threading

from constants.path import BUILTIN_TYPES

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
        def compile_thread():
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(self.source)
                tmp_file_path = f.name

            compile_command = ['pyinstaller', '--noconfirm', '--log-level=ERROR', '--name', f'{self.filename}.exe', '--onefile', tmp_file_path]
            subprocess.run(compile_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            os.remove(tmp_file_path) 

        # Start the compilation in a separate thread
        thread = threading.Thread(target=compile_thread)
        thread.start()

    def run(self):
        # Ensure this method is thread-safe if interacting with the GUI
        exe_path = Path("./dist") / f"{self.filename}.exe"
        if exe_path.exists():
            # Command to open a new cmd prompt and run the executable
            run_command = f'cmd /c start cmd.exe /k "{exe_path}"'
            threading.Thread(target=lambda: subprocess.run(run_command, shell=True)).start()
        else:
            print("Executable not found.") # for debugging
        
    def run_python(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.source)
            tmp_file_path = f.name
        subprocess.run(['python', tmp_file_path])
        os.remove(tmp_file_path)

    def builtins(self) -> str:
        with open(BUILTIN_TYPES, 'r') as f:
            contents = f.read()
        return contents
