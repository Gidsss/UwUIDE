"""
This script serves a package manager that mainly checks dependencies and run subprocesses for install, build, and test.

To use this, simply run this command in the command line:

    python -m run < install | uninstall | build | test > < optional params >
"""

import sys
import subprocess
import importlib
from pathlib import Path

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

# Install dependencies
def install(pm: PackageManager, package_name = None) -> None:
    """
    This function can install packages from requirements.txt or one by one.

    python -m run install
    python -m run install < package name >
    """
    pm.check_dependency('pip')
    commands = ['pip', 'install']

    if package_name is not None:
        pm.run_subprocess(commands, package_name)
    else:
        pm.run_subprocess([*commands, '-r'], 'requirements.txt')

# Uninstall dependencies
def uninstall(pm: PackageManager, package_name = None) -> None:
    """
    This function can uninstall packages from requirements.txt or one by one.

    python -m run uninstall
    python -m run uninstall < package name >
    """
    pm.check_dependency('pip')
    commands = ['pip', 'uninstall']

    if package_name is not None:
        pm.run_subprocess(commands, package_name)
    else:
        pm.run_subprocess([*commands, '-r'], 'requirements.txt')

# Run IDE
def build(pm: PackageManager) -> None:      
    """
    This function can build the UwU IDE.

    python -m run build
    """  
    pm.run_subprocess([sys.executable, '-m'], 'src.uwu')

# Run pytest
def test(pm: PackageManager, filename = None) -> None:
    """
    This function can run pytest.

    python -m run test
    python -m run test test_*
    python -m run test *_test
    """
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
        globals()[args[0]](pm, *args[1:])
    except KeyError:
        raise KeyError(f"Cannot call function {args[0]}. It should be of type (install | build | test)")