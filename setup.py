from setuptools import setup, find_packages

setup(
    name = "tcharmap",
    version = "0.1",
    packages = ['tcharmap', 'tcharmap.resources'],
    package_data = {
        'tcharmap': ['charmap']
    },
    install_requires = "PyYAML"
)
