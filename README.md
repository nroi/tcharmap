tcharmap is a simple GUI that provides an overview of unicode characters and
their LaTeX counterpart. The mappings are mostly based on
http://www.w3.org/Math/characters/unicode.xml.

## Requirements
* Python3
* PyQt5
* [PyYAML](https://pypi.python.org/pypi/PyYAML/3.11)

## Usage
Start typing what you're looking for. You can enter a single unicode character
(e.g. α) in order to find the LaTeX counterpart or some text that is part of the
description (e.g. alpha).

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
