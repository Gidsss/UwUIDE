from setuptools import setup

setup(
    name='uwu',
    version='0.0.1',
    author='SenPys',
    entry_points={
        'console_scripts':[
            'uwu=uwu.main:run'
        ]
    }
)