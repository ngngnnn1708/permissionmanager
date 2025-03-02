import mysql.connector
import pandas as pd

class PermissionManager:
    def __init__(self, host ="127.0.0.1", user ="root", password ="ngocnam170898@", database="user_management"):
        """Khởi tạo kết nối MySQL"""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Lỗi kết nối MySQL: {err}")
            self.conn = None
    
    def list_permission(self):
        """Liệt kê danh sách tất cả các quyền"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "SELECT ID, Name, Description FROM mor_permission"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return pd.DataFrame(data) if data else pd.DataFrame(columns=["ID", "Name", "Description"])
        except mysql.connector.Error as err:
            return {"message": f"Lỗi {err}", "status": "error"}
    
    def add_permission(self, permission_id, name, description):
        """Thêm quyền mới vào bảng mor_permission"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "INSERT INTO mor_permission (ID, Name, Description) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (permission_id, name, description))
            self.conn.commit()
            return {"message": "Thêm quyền thành công!", "status": "success"}
        except mysql.connector.IntegrityError:
            return {"message": "ID đã tồn tại!", "status": "error"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def delete_permission(self, permission_id):
        """Xóa quyền trong bảng mor_permission"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "DELETE FROM mor_permission WHERE ID = %s"
            self.cursor.execute(sql, (permission_id,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"message": "Không tìm thấy quyền!", "status": "error"}
            return {"message": "Xóa quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def update_permission(self, permission_id, name, description):
        """Cập nhật thông tin quyền theo ID"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "UPDATE mor_permission SET name = %s, description = %s WHERE ID = %s"
            self.cursor.execute(sql, (name, description, permission_id))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"message": "Không tìm thấy quyền!", "status": "error"}
            return {"message": "Cập nhật quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()