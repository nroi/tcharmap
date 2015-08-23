from setuptools import setup, find_packages

setup(
    name = "pycharmap",
    version = "0.1",
    packages = ['pycharmap'],
    package_data = {
        'pycharmap': ['charmap']
    },
    py_modules = ['__main__'],
    install_requires = "PyYAML"
)
