from invoke import task

@task
def test(c, file = None):
    print('Running Tests...')
    if file is not None:
        print(file)
        c.run(f"python -m pytest test/{file}")
    else:
        c.run('python -m pytest test/')

@task
def build(c):
    print('Building UwU++ IDE...')
    c.run('python -m src.uwu')