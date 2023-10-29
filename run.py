"""
This script serves a package manager that mainly checks dependencies and run subprocesses for install, build, and test.

To use this, simply run this command in the command line:

    python -m run < subprocess_name > < optional params >
"""

import sys
import subprocess
import importlib

class PackageManager():
    def run_subprocess(self, commands: list[str], script) -> None:
        try:
            subprocess.run([*commands, script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def check_dependency(self, package_name: str):
        print(f"Checking {package_name}...")
        try:
            importlib.import_module(package_name)
            print(f"{package_name} is installed.")
        except ImportError:
            raise ImportError(f"{package_name} is not installed!")

# Instal dependencies
def install(pm: PackageManager) -> None:
    pm.check_dependency('pip')
    pm.run_subprocess(['pip', 'install', '-r'], 'requirements.txt')

# Run IDE
def build(pm: PackageManager) -> None:        
    pm.run_subprocess([sys.executable, '-m'], 'src.uwu')

# Run pytest
def test(pm: PackageManager, filename = None) -> None:
    pm.check_dependency('pytest')

    script = 'test/'

    if filename is not None:
        script += f"{filename}.py"
    
    pm.run_subprocess(["pytest"], script)

if __name__ == '__main__':
    pm = PackageManager()
    args = sys.argv[1:]

    if len(args) == 0:
        raise TypeError("Please specify which script to run. (install | build | test)")
    
    try:
        globals()[args[0]](pm=pm, *args[1:])
    except KeyError:
        raise KeyError(f"Cannot call function {args[0]}. It should be of type (install | build | test)")