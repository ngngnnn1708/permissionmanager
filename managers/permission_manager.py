import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

class PermissionManager:
    def __init__(self, host=None, user=None, password=None, database=None):
        """Khởi tạo kết nối MySQL"""
        load_dotenv()
        try:
            self.conn = mysql.connector.connect(
                host=host or os.getenv("DB_HOST", "127.0.0.1"),
                user=user or os.getenv("DB_USER", "root"),
                password=password or os.getenv("DB_PASSWORD"),
                database=database or os.getenv("DB_NAME", "user_management")
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Lỗi kết nối MySQL: {err}")
            self.conn = None
 # ==================== QUẢN LÝ QUYỀN ====================   
    def list_permission(self):
        """Liệt kê danh sách tất cả các quyền"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "SELECT id, name, description FROM mor_permission"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data if data else []
        except mysql.connector.Error as err:
            return {"message": f"Lỗi {err}", "status": "error"}
    
    def add_permission(self, name, description):
        """Thêm quyền mới vào bảng mor_permission"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Kiểm tra quyền đã tồn tại chưa
            check_sql = "SELECT COUNT(*) as count FROM mor_permission WHERE name = %s"
            self.cursor.execute(check_sql, (name,))
            if self.cursor.fetchone()["count"] > 0:
                return {"message": "Quyền đã tồn tại!", "status": "error"}

            sql = "INSERT INTO mor_permission (name, description) VALUES (%s, %s)"
            self.cursor.execute(sql, (name, description))
            self.conn.commit()
            return {"message": "Thêm quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def delete_permission(self, permission_id):
        """Xóa quyền trong bảng mor_permission"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Kiểm tra quyền có tồn tại hay không
            check_sql = "SELECT id FROM mor_permission WHERE id = %s"
            self.cursor.execute(check_sql, (permission_id,))
            if not self.cursor.fetchone():
                return {"message": "Không tìm thấy quyền!", "status": "error"}

            sql = "DELETE FROM mor_permission WHERE id = %s"
            self.cursor.execute(sql, (permission_id,))
            self.conn.commit()
            return {"message": "Xóa quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def update_permission(self, permission_id, name, description):
        """Cập nhật thông tin quyền theo ID"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Kiểm tra quyền có tồn tại không
            check_sql = "SELECT id FROM mor_permission WHERE id = %s"
            self.cursor.execute(check_sql, (permission_id,))
            if not self.cursor.fetchone():
                return {"message": "Không tìm thấy quyền!", "status": "error"}

            sql = "UPDATE mor_permission SET name = %s, description = %s WHERE id = %s"
            self.cursor.execute(sql, (name, description, permission_id))
            self.conn.commit()
            return {"message": "Cập nhật quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()