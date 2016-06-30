tcharmap is a simple GUI that provides an overview of unicode characters and
their LaTeX counterpart. The mappings are mostly based on
http://www.w3.org/Math/characters/unicode.xml.

![tcharmap](https://raw.githubusercontent.com/nrio0/tcharmap/master/tcharmap.png)

## Requirements
* Python3
* PyQt5
* [PyYAML](https://pypi.python.org/pypi/PyYAML/3.11)

## Install

For ArchLinux, a package can be found on [AUR](https://aur.archlinux.org/packages/tcharmap-git/).
For all other distributions, the package can be built using setuptools. For
example, on Ubuntu:
```
sudo apt-get install python3-setuptools
sudo apt-get install python3-yaml
sudo apt-get install python3-pyqt5
git clone https://github.com/nrio0/tcharmap.git
cd tcharmap
python3 setup.py bdist_egg
```

The resulting egg file can be executed directly with python using:
```
python3 dist/tcharmap-0.1-py3.5.egg
```

## Usage
Start typing what you're looking for.
If you want a specific unicode character and you happen to remember its LaTeX
representation, just type the LaTeX representation (e.g. "infty" for the
infinity symbol ∞). Conversely, you can enter the unicode representation ∞ to
find its LaTeX representation, i.e, "\infty".

hjkl-based movements are supported: Hit \<TAB\> in order to switch focus to the
results, choose the desired result with the hjkl keys. The currently selected cell can be
automatically copied by setting 'auto\_copy' to True: Create a yaml file
```
auto_copy:
    True
```
and save it in $XDG\_CONFIG\_HOME/tcharmap/settings.yaml (if you're not on
Linux, replace $XDG\_CONFIG\_HOME by whatever is being used on your operating
system for application settings).
