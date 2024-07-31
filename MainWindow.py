import sys
import sqlite3

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QMessageBox, QTableWidgetItem, QFileDialog


from SanPham import SanPham
from DatabaseManager import DatabaseManager
from QLSP_UI import Ui_MainWindow

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)

        self.uic.btnDelete.clicked.connect(self.Delete)
        self.uic.btnExport.clicked.connect(self.Export)
        self.uic.btnTimKiem.clicked.connect(self.callSearch)
        self.uic.tbSanPham.cellClicked.connect(self.table_item_clicked)

        self.db_Path = "D:\\Learn\\Phat_trien_van_hanh_va_BTPM\\KTGK\\qlsp.db"
        self.db_Manager = DatabaseManager(self.db_Path)
        self.Load_Data()

    def callSearch(self):
        tenSPCanTim = self.uic.txNhapSP.toPlainText()
        print(f"Tên sản phẩm cần tìm: {tenSPCanTim}")
        try:
            dsSanPham = self.db_Manager.Search_Product(tenSPCanTim)
            self.uic.tbSanPham.setColumnCount(6)
            self.uic.tbSanPham.setRowCount(len(dsSanPham))
            self.uic.tbSanPham.setHorizontalHeaderLabels(['ID', 'MaSP', 'TenSP', 'TinhTrang', 'GiaNhap', 'SoLuong'])
            for row, SanPham in enumerate(dsSanPham):
                for column, data in enumerate(SanPham):
                    self.uic.tbSanPham.setItem(row, column, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
        except Exception as e:
            print(f"Lỗi xử lý dữ liệu: {e}")
            
    def Delete(self):
        idsp = self.uic.txID.toPlainText()
        self.db_Manager.Delete_Product(idsp)
        self.Load_Data()

    def Export(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self.main_win, "Export File", "", "Text Files (*.txt)")
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    for row in range(self.uic.tbSanPham.rowCount()):
                        data = [self.uic.tbSanPham.item(row, column).text() for column in range(self.uic.tbSanPham.columnCount())]
                        file.write('\t'.join(data) + '\n')
                QMessageBox.information(self.main_win, "Export Successful", "Data exported successfully.")
        except Exception as e:
            print(f"Lỗi xuất dữ liệu: {e}")
            QMessageBox.critical(self.main_win, "Lỗi", f"Lỗi xuất dữ liệu: {e}")
    
    def table_item_clicked(self):
        try:
            row = self.uic.tbSanPham.currentRow()
            self.uic.txID.setText(self.uic.tbSanPham.item(row, 0).text())
            self.uic.txMaSP.setText(self.uic.tbSanPham.item(row, 1).text())
            self.uic.txTenSP.setText(self.uic.tbSanPham.item(row, 2).text())
            self.uic.txTinhTrang.setText(self.uic.tbSanPham.item(row, 3).text())
            self.uic.txGiaNhap.setText(self.uic.tbSanPham.item(row, 4).text())
            self.uic.txSoLuong.setText(self.uic.tbSanPham.item(row, 5).text())
        except Exception as e:
            print(f"Lỗi xử lý dữ liệu: {e}")
            QMessageBox.critical(self.main_win, "Lỗi", f"Lỗi xử lý dữ liệu: {e}")
            
    def Load_Data(self):
        try:
            dsSanPham = self.db_Manager.Get_Products()
            self.uic.tbSanPham.setColumnCount(6)
            self.uic.tbSanPham.setRowCount(len(dsSanPham))
            self.uic.tbSanPham.setHorizontalHeaderLabels(['ID', 'MaSP', 'TenSP', 'TinhTrang', 'GiaNhap', 'SoLuong'])
            for row, SanPham in enumerate(dsSanPham):
                for column, data in enumerate(SanPham):
                    self.uic.tbSanPham.setItem(row, column, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
            QMessageBox.critical(self.main_win, "Lỗi", f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
        except Exception as e:
            print(f"Lỗi xử lý dữ liệu: {e}")
            QMessageBox.critical(self.main_win, "Lỗi", f"Lỗi xử lý dữ liệu: {e}")
    def show(self):
        self.main_win.show()

def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

