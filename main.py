import datetime
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox, QHeaderView


class MWindow(QMainWindow):

    def __init__(self):
        super(MWindow, self).__init__()
        uic.loadUi("main.ui", self)

        self.db = sqlite3.connect("coffee.sqlite")
        self.loadFromDB()
    
    def delete(self):
        r = self.tableWidgetcurrentRow()
        if r == -1:
            QMessageBox.warning(self, "Внимание", "Не выбран кофе для удаления")
            return
        
        ii = int(self.tableWidgetitem(r, 0).text())
        n = self.tableWidgetitem(r, 1).text()
        r = QMessageBox.question(self, "Вы уверены?", f"Удалить кофе {n}?", QMessageBox.Yes, QMessageBox.No)
        if r == QMessageBox.Yes:
            self.db.cursor().execute(f"DELETE from coffee WHERE id = {ii}")
            self.loadFromDB()
    
    def loadFromDB(self):
        query = "SELECT * FROM coffee ORDER BY id ASC"
        res = self.db.cursor().execute(query).fetchall()
        headers = "ID, Название сорта, Степень обжарки, Тип, Описание вкуса, Цена, Объем упаковки".split(", ")
        
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    elem = "Молотый" if elem == "TRUE" else "Зерновой"
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def closeEvent(self, e):
        self.db.close()

            
sys.excepthook = lambda c, e, t: sys.__excepthook__(c, e, t)
app = QApplication(sys.argv)
ex = MWindow()
ex.show()
sys.exit(app.exec())
    
