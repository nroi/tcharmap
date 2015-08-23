#!/usr/bin/env python

## TODO exclude ascii signs, including < (breaks html files)

import xml.etree.ElementTree as ET

def hex_to_char(s):
    """Return the unicode string of the 5-digit hex codepoint."""
    return chr(int(s[1:], 16))

def main():
    tree = ET.parse('unicode.xml')
    root = tree.getroot()
    for child in root:
        try:
            if child.tag == 'character' and child.attrib['mode'] == 'math':
                unicode_id = child.attrib['id']
                if len(unicode_id) == 6:    # skip unicode ranges
                    latex = child.find('latex')
                    description = child.find('description')
                    if latex is not None and description is not None:
                        char = hex_to_char(unicode_id)
                        if ord(char) > 127:
                            print(char, latex.text, description.text)
        except KeyError:
            pass

if __name__ == "__main__":
    main()
