import platform
from invoke import task

SYSTEM = platform.system()
COMMAND = "python"

if SYSTEM == 'Darwin': # for macOS
    COMMAND = 'python3'

@task
def install(c):
    c.run(f"{COMMAND} -m pip install -r requirements.txt")
    
@task
def test(c, file = None):
    print('Running Tests...')
    if file is not None:
        print(file)
        c.run(f"{COMMAND} -m pytest test/{file}")
    else:
        c.run(f"{COMMAND} -m pytest test/")

@task
def build(c):
    print('Building UwU++ IDE...')
    
    c.run(f"{COMMAND} -m src.uwu")