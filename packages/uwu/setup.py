from setuptools import setup

setup(
    name='uwu',
    version='0.2.1',
    author='SenPys',
    description='Console script package for UwU IDE',
    entry_points={
        'console_scripts':[
            'uwu=main:run'
        ]
    }
)