"""Overview of unicode characters and their LaTeX counterpart"""

from PyQt5.QtCore import Qt                     # pylint: disable=E0611
from PyQt5.QtCore import QEvent                 # pylint: disable=E0611
from PyQt5.QtWidgets import QDialog             # pylint: disable=E0611
from PyQt5.QtWidgets import QApplication        # pylint: disable=E0611
from PyQt5.QtWidgets import QLineEdit           # pylint: disable=E0611
from PyQt5.QtWidgets import QVBoxLayout         # pylint: disable=E0611
from PyQt5.QtWidgets import QTableWidget        # pylint: disable=E0611
from PyQt5.QtWidgets import QTableWidgetItem    # pylint: disable=E0611
from PyQt5 import QtGui

import sys
import os
import yaml
import platform
from pkg_resources import resource_string

import tcharmap.resources.icons_rc

def get_config_home():
    """Returns the directory used for application settings"""
    if platform.system() == 'Linux':
        try:
            return os.environ.get('XDG_CONFIG_HOME', None) or os.environ['HOME']
        except KeyError:
            raise KeyError("Neither $XDG_CONFIG_HOME nor $HOME is defined")
    elif platform.system() == 'Windows':
        return os.environ['appdata']
    elif platform.system() == 'Darwin':
        return os.path.join(os.environ['HOME'], 'Library', 'Preferences')
    else:
        try:
            return os.environ.get('XDG_CONFIG_HOME', None) or os.environ['HOME']
        except KeyError:
            print("{} is not supported. Sorry!".format(platform.system()))
            sys.exit()

def user_defined_descriptions(path):
    """Returns a dict consisting of (unicode_char, description) tuples"""
    try:
        lines = [line.rstrip() for line in open(path).readlines()]
        return dict([x.split(maxsplit=1) for x in lines])
    except FileNotFoundError:
        return dict()

def read_entries():
    """Parses the included file into its entries"""
    entries = []
    user_dict = user_defined_descriptions(
        os.path.join(get_config_home(), 'tcharmap', 'descriptions'))
    charmap_txt = resource_string(__name__, 'charmap').decode('utf-8')
    lines = charmap_txt.split('\n')[:-1]  # discard last newline
    for line in lines:
        char, latex, description = line.strip().split(maxsplit=2)
        user_description = user_dict.get(char, None)
        entries.append((char, latex, description, user_description))
    return entries

class VLineEdit(QLineEdit):
    """QLineEdit with vim-like CTRL-U and CTRL-W shortcuts"""
    def keyPressEvent(self, event):
        if (event.type() == QEvent.KeyPress
                and event.key() == Qt.Key_W
                and event.modifiers() == Qt.ControlModifier):
            while self.text() and self.text()[self.cursorPosition() - 1].isspace():
                self.backspace()
            while self.text() and not self.text()[self.cursorPosition() - 1].isspace():
                self.backspace()
        elif (event.type() == QEvent.KeyPress
              and event.key() == Qt.Key_U
              and event.modifiers() == Qt.ControlModifier):
            self.setText("")
        super().keyPressEvent(event)


class Form(QDialog):
    """The main window used to display all entries"""

    def eventFilter(self, obj, event):
        """intercept hjkl-keys"""
        if obj == self.table and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_H:
                new_col = max(0, self.table.currentColumn() - 1)
                self.table.setCurrentCell(self.table.currentRow(), new_col)
                return True
            elif event.key() == Qt.Key_J:
                new_row = min(self.table.rowCount() - 1, self.table.currentRow() + 1)
                self.table.setCurrentCell(new_row, self.table.currentColumn())
                return True
            elif event.key() == Qt.Key_K:
                new_row = max(0, self.table.currentRow() - 1)
                self.table.setCurrentCell(new_row, self.table.currentColumn())
                return True
            elif event.key() == Qt.Key_L:
                new_col = min(2, self.table.currentColumn() + 1)
                self.table.setCurrentCell(self.table.currentRow(), new_col)
                return True
            elif event.key() == Qt.Key_Tab:
                self.lineedit.setFocus()
                return True
        return False

    def lookup(self, term):
        """Return a list with all entries matching the given term"""
        results = []
        lookup_term = term.lower()
        for char, latex, description, user_description in self.entries:
            if (char == term or
                    latex[1:].startswith(lookup_term) or
                    lookup_term in description.lower() or
                    (user_description and lookup_term in user_description)):
                results.append((char, latex, description, user_description))
        return results

    def update_query(self):
        """Update results and reset x-y coordinates"""
        text = self.lineedit.text()
        self.results = self.lookup(text)
        self.update_ui()
        self.copy_entry(self.table.currentRow(), self.table.currentColumn())

    def __init__(self, settings, parent=None):
        super(Form, self).__init__(parent)
        icon = QtGui.QIcon(":/tcharmap.png")
        self.setWindowIcon(icon)
        self.settings = settings
        self.results = []
        self.entries = read_entries()
        self.lineedit = VLineEdit()
        self.lineedit.selectAll()
        self.table = QTableWidget()
        self.table.installEventFilter(self)
        self.table.currentCellChanged[int, int, int, int].connect(self.copy_entry_slot)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.textChanged[str].connect(self.update_query)
        self.lineedit.setFocus()
        self.setWindowTitle("tcharmap")
        self.results = self.lookup("")
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setColumnWidth(1, 150)
        self.clipboard = QApplication.clipboard()
        self.resize(540, 530)
        self.update_ui()

    def copy_entry(self, row, col):
        """Copy the currently selected entry"""
        if self.results and self.settings['auto_copy']:
            row, col = self.table.currentRow(), self.table.currentColumn()
            to_copy = self.results[row][col]
            self.clipboard.setText(to_copy)

    def copy_entry_slot(self, row, col, prev_row, prev_col):
        self.copy_entry(row, col)

    def update_ui(self):
        """Update the UI with all entries contained in self.results"""
        if self.results:
            self.table.setRowCount(len(self.results))
            for idx, item in enumerate(self.results):
                char, latex, description, user_description = item
                char_item = QTableWidgetItem(char)
                char_item.setFlags(char_item.flags() & ~Qt.ItemIsEditable)
                latex_item = QTableWidgetItem(latex)
                latex_item.setFlags(latex_item.flags() & ~Qt.ItemIsEditable)
                user_desc = " [{}]".format(user_description) if user_description else ""
                description_item = QTableWidgetItem("{}{}".format(description, user_desc))
                description_item.setFlags(description_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(idx, 0, char_item)
                self.table.setItem(idx, 1, latex_item)
                self.table.setItem(idx, 2, description_item)
            self.table.setCurrentCell(0, 0)
        else:
            self.table.setRowCount(0)

def get_settings():
    """Returns a dictionary containing all settings"""
    settings_path = os.path.join(get_config_home(), 'tcharmap', 'settings.yaml')
    try:
        return yaml.load(open(settings_path))
    except FileNotFoundError:
        return {'auto_copy': False}

def main():
    app = QApplication(sys.argv)
    form = Form(get_settings())
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
