import datetime
import sqlite3
import sys
from mainui import Ui_MainWindow
from addEditCoffeeForm import Ui_Dialog

from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QTableWidgetItem, QHeaderView, QMessageBox


class MWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MWindow, self).__init__()
        self.setupUi(self)

        self.db = sqlite3.connect("data/coffee.sqlite")
        self.loadFromDB()
        self.pushButton_3.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.pushButton.clicked.connect(self.delete)
    
    def add(self):
        self.www = MultiWindow(self, "Добавить")
        self.www.show()
    
    def edit(self):
        r = self.tableWidget.currentRow()
        if r == -1:
            QMessageBox.warning(self, "Внимание", "Не выбран кофе для редактирования")
            return
        ii = int(self.tableWidget.item(r, 0).text())
        
        self.www = MultiWindow(self, "Изменить", r, ii)
        self.www.show()
    
    def delete(self):
        r = self.tableWidget.currentRow()
        if r == -1:
            QMessageBox.warning(self, "Внимание", "Не выбран кофе для удаления")
            return
        
        ii = int(self.tableWidget.item(r, 0).text())
        n = self.tableWidget.item(r, 1).text()
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
                if elem is None:
                    elem = " "
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def closeEvent(self, e):
        self.db.close()


class MultiWindow(QDialog, Ui_Dialog):
    
    def __init__(self, main, text, row=-1, dbid=-1):
        super(MultiWindow, self).__init__()
        self.setupUi(self)
        self.mainwindow = main
        self.setWindowTitle(f"{text} кофе")
        
        self.buttonBox.accepted.connect(self.add)
        self.dbid = dbid
        if dbid != -1:
            for i in range(6):
                t = self.mainwindow.tableWidget.item(row, i + 1).text()
                a = getattr(self, f"lineEdit_{i + 1}") if i != 2 else 0
                (a.setText(t) if i != 2 else (self.radioButton.setChecked(1) if t == "Молотый" else self.radioButton_2.setChecked(1)))
        
    def add(self):
        p = "name, roast, milled, description, price, pack_size".split(", ")
        v = [getattr(self, f"lineEdit_{i + 1}").text() if i != 2 else 0 for i in range(6)]
        v[2] = str(self.radioButton.isChecked()).upper()
        cur = self.mainwindow.db.cursor()
        if self.dbid == -1:
            i = cur.execute("SELECT id FROM coffee ORDER BY id DESC LIMIT 1").fetchone()[0] + 1
            cur.execute(f"INSERT INTO coffee({', '.join(p)}) VALUES ({', '.join(v)})")
        else:
            i = self.dbid
            kv = ", ".join([f"{p[i]} = '{v[i]}'" for i in range(len(p))])
            cur.execute(f"UPDATE coffee SET {kv} WHERE id = {i}")
        self.close()
        self.mainwindow.loadFromDB()

            
sys.excepthook = lambda c, e, t: sys.__excepthook__(c, e, t)
app = QApplication(sys.argv)
ex = MWindow()
ex.show()
sys.exit(app.exec())
    
