import sqlite3
class DatabaseManager:
    def __init__(self, qlsp):
        self.qlsp = qlsp

    def Get_Products(self):
        try:
            conn = sqlite3.connect(self.qlsp)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SanPham")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
            return []

    def Search_Product(self, tenSPCanTim):
        try:
            # Kết nối đến cơ sở dữ liệu
            conn = sqlite3.connect(self.qlsp)
            cursor = conn.cursor()
            # Tìm kiếm sản phẩm theo tên
            queryTimKiem = "SELECT * FROM SanPham WHERE TenSP LIKE ?"
            cursor.execute(queryTimKiem, (f"%{tenSPCanTim}%",))
            rows = cursor.fetchall()
            conn.close()
            # In số lượng sản phẩm tìm được
            print(f"Số lượng sản phẩm tìm được: {len(rows)}")
            return rows
        except sqlite3.Error as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
            return []

    def Add_Product(self, sp):
        try:
            conn = sqlite3.connect(self.qlsp)
            cursor = conn.cursor()
            queryThem = "INSERT INTO SanPham (MaSP, TenSP, TinhTrang, GiaNhap, SoLuong) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(queryThem, (sp.maSP, sp.tenSP, sp.tinhTrang, sp.giaNhap, sp.soLuong))
            conn.commit()
            conn.close()
            print(f"Thêm sản phẩm {sp.tenSP} thành công!")
        except sqlite3.Error as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")

    def Delete_Product(self, idsp):
        try:
            conn = sqlite3.connect(self.qlsp)
            cursor = conn.cursor()
            queryXoa = ("DELETE FROM SanPham WHERE ID = ?")
            cursor.execute(queryXoa, (idsp,))
            conn.commit()
            conn.close()
            print("Xóa sản phẩm", idsp, "thành công!")
        except sqlite3.Error as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")