from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QHBoxLayout, \
    QLayout

import dedup
import sys
from FileService import FileService
from ImageLabel import ImageLabel
from iconribbon.IconRibbon import IconRibbon


class DeDup(QMainWindow, dedup.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.folderButton.clicked.connect(self.browse_for_folder)
        self.searchProgress.hide()
        self.searchButton.clicked.connect(self.search_clicked)
        self.icon_button_x = 60
        self.count_of_files = 0
        self.displayGridFrame.hide()
        self.searchProgress.hide()
        self.resultsFrame.hide()
        self.first_image_displayed = False
        self.image_label = None
        self.files_to_delete = []
        self.deleteButton.clicked.connect(self.delete_button_clicked)
        self.actual_list_of_all_duplicates = []
        self.ribbonLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.ribbonLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.icon_ribbon = IconRibbon(self.ribbonLayout)

    def browse_for_folder(self):
        file = str(
            QFileDialog.getExistingDirectory(self, "Select Directory",
                                             directory="/Users/solomon/Documents/Amazon/Amazon Photos Downloads"))
        self.folderList.addItem(file)
        self.folderList.keyPressEvent = self.key_entered_on_list

    def key_entered_on_list(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.remove_item_from_list()

    def remove_item_from_list(self):
        listItems = self.folderList.selectedItems()
        if not listItems: return
        for item in listItems:
            self.folderList.takeItem(self.folderList.row(item))

    def search_clicked(self):
        self.searchProgress.show()
        self.searchProgress.setValue(1)
        potential_dup_files = []
        for index in range(self.folderList.count()):
            potential_dup_files = potential_dup_files + FileService.get_list_of_potential_duplicate_files(
                self.folderList.item(index).text())
        self.count_of_files = len(potential_dup_files)
        all_files = FileService.get_dict_of_all_files_by_size(potential_dup_files)
        self.start_analyzing_potential_duplicates(all_files)

    def start_analyzing_potential_duplicates(self, all_files):
        files_processed = 0
        self.actual_list_of_all_duplicates = []
        for key, value in all_files.items():
            files_processed += len(value)
            if len(value) > 1:
                self.actual_list_of_all_duplicates.append(FileService.get_duplicates_in_list(value))
            self.searchProgress.setValue((files_processed / self.count_of_files) * 100)
            QApplication.processEvents()
        self.add_image_icons()

    def add_image_icons(self):
        for dup_files in self.actual_list_of_all_duplicates:
            self.add_icon_button(dup_files)
        self.searchProgress.hide()

    def add_icon_button(self, dup_files):
        self.icon_ribbon.add_icon(dup_files[0].name, lambda e: self.image_clicked(dup_files))

    def image_clicked(self, dup_files):
        if self.first_image_displayed:
            self.display_subsequent_image(dup_files)
        else:
            self.display_first_image(dup_files)
            self.first_image_displayed = True
        self.resultsFrame.show()
        self.resultsTable.setRowCount(len(dup_files))
        self.resultsTable.resizeColumnToContents(0)
        i = 0
        for dup in dup_files:
            self.add_duplicate_folder_to_table(dup, i)
            i += 1
        self.resultsTable.resizeColumnsToContents()
        self.resultsTable.itemClicked.connect(self.duplicate_item_clicked)
        self.deleteButton.setEnabled(False)

    def add_duplicate_folder_to_table(self, dup, index):
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        chkBoxItem.setCheckState(Qt.CheckState.Unchecked)
        item = QTableWidgetItem(dup.name)
        self.resultsTable.setItem(index, 0, chkBoxItem)
        self.resultsTable.setItem(index, 1, item)

    def display_first_image(self, dup_files):
        self.displayGridFrame.show()
        self.image_label = ImageLabel(dup_files[0].name)
        self.displayLayout.addWidget(self.image_label)
        self.displayLayout.setRowStretch(0, 1)
        self.displayLayout.setColumnStretch(0, 1)
        self.first_image_displayed = True

    def display_subsequent_image(self, dup_files):
        self.displayGridFrame.show()
        self.image_label.changePixmap(dup_files[0].name)

    def duplicate_item_clicked(self, item: QTableWidgetItem):
        self.files_to_delete = []
        for row in range(self.resultsTable.rowCount()):
            if self.resultsTable.item(row, 0).checkState() == Qt.CheckState.Checked:
                self.files_to_delete.append(self.resultsTable.item(row, 1).text())
        self.deleteButton.setEnabled(len(self.files_to_delete) > 0)

    def delete_button_clicked(self):
        if len(self.files_to_delete) == 0:
            return
        while self.files_to_delete:
            file = self.files_to_delete.pop(0)
            FileService.delete_file(file)
            self.remove_file_from_list(file)

    def remove_file_from_list(self, file):
        _redraw_ribbon = False
        for row in range(self.resultsTable.rowCount()):
            if self.resultsTable.item(row, 1).text() == file:
                self.resultsTable.removeRow(row)
                break
        _index = -1
        for i in range(len(self.actual_list_of_all_duplicates)):
            for j in range(len(self.actual_list_of_all_duplicates[i])):
                if self.actual_list_of_all_duplicates[i][j].name == file:
                    self.actual_list_of_all_duplicates[i].pop(j)
                    break

            if len(self.actual_list_of_all_duplicates[i]) == 1:
                self.actual_list_of_all_duplicates.pop(i)
                self.displayGridFrame.hide()
                _redraw_ribbon = True
                _index = i
                break
        if _redraw_ribbon:
            self.remove_icon_from_ribbon(_index)

    def remove_icon_from_ribbon(self, index):
        self.icon_ribbon.remove_icon(index)


app = QApplication(sys.argv)
main = DeDup()
main.show()
sys.exit(app.exec())
