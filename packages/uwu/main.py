"""
This script serves a package manager that mainly checks dependencies and run subprocesses for install, uninstall, build, and test.

To use this, simply run this command in the command line:

    uwu < install | uninstall | build | test > < optional params >
"""

import sys
import subprocess
import importlib

class ConsoleTools():
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
    
    def update_requirements(self):
        proc = subprocess.Popen(['pip', 'freeze'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output, _ = proc.communicate()
        clean_output = "\n".join(line.strip() for line in output.decode().split('\n'))

        with open('requirements.txt', 'w') as file:
            file.write(clean_output)

# Install dependencies
def install(ct: ConsoleTools, package_name = None) -> None:
    """
    This function can install packages from requirements.txt or one by one.

    uwu install
    uwu install < package name >
    """
    ct.check_dependency('pip')
    commands = ['pip', 'install']

    if package_name is not None:
        ct.run_subprocess(commands, package_name)
        ct.update_requirements()
    else:
        ct.run_subprocess([*commands, '-r'], 'requirements.txt')

# Uninstall dependencies
def uninstall(ct: ConsoleTools, package_name = None) -> None:
    """
    This function can uninstall packages from requirements.txt or one by one.

    uwu uninstall
    uwu uninstall < package name >
    """
    ct.check_dependency('pip')
    commands = ['pip', 'uninstall']

    if package_name is not None:
        ct.run_subprocess(commands, package_name)
        ct.update_requirements()
    else:
        ct.run_subprocess([*commands, '-r'], 'requirements.txt')

def lexer(ct: ConsoleTools) -> None:
    """
    This function can run lexer package.

    uwu lexer
    """  
    print('Running lexer package...')
    ct.run_subprocess([sys.executable, '-m'], 'src.lexer')

# Run IDE
def build(ct: ConsoleTools) -> None:      
    """
    This function can build the UwU IDE.

    uwu build
    """ 
    print('Building UwU IDE...')
    ct.run_subprocess([sys.executable, '-m'], 'src.uwu')
    print('Build successful...')

# Run pytest
def test(ct: ConsoleTools, filename = None) -> None:
    """
    This function can run pytest.

    uwu test
    uwu test test_*
    uwu test *_test
    """
    ct.check_dependency('pytest')

    script = 'test/'

    if filename is not None:
        script += f"{filename}.py"
    
    ct.run_subprocess(["pytest"], script)

def run():
    ct = ConsoleTools()
    args = sys.argv[1:]

    if len(args) == 0:
        raise TypeError("Please specify which script to run. (install | uninstall | build | test)")
    
    try:
        globals()[args[0]](ct, *args[1:])
    except KeyError:
        raise KeyError(f"Cannot call function {args[0]}. It should be of type (install | uninstall | build | test)")