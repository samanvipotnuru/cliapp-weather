from importlib.metadata import entry_points
from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt") as readFile:
        content = readFile.read()
        requirements = content.split('\n')
    return requirements


setup(
    name = "myapp",
    version = "0.1",
    packages = find_packages(),
    include_package_data=True,
    install_requires = read_requirements(),entry_points='''
    [console_scripts]
    myapp = myapp.cli:entry
    '''
)