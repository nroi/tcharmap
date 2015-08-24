from setuptools import setup, find_packages

setup(
    name = "tcharmap",
    version = "0.1",
    packages = ['tcharmap'],
    package_data = {
        'tcharmap': ['charmap']
    },
    py_modules = ['__main__'],
    install_requires = "PyYAML"
)
