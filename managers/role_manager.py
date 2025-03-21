import mysql.connector
import os
from dotenv import load_dotenv

class RoleManager:
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

    def list_roles(self):
        """Liệt kê tất cả vai trò"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "SELECT id, name, description FROM mor_role"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data if data else []
        except mysql.connector.Error as err:
            return {"message": f"Lỗi {err}", "status": "error"}

    def add_role(self, name, description):
        """Thêm vai trò mới vào bảng mor_role"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "INSERT INTO mor_role (name, description) VALUES (%s, %s)"
            self.cursor.execute(sql, (name, description))
            self.conn.commit()
            return {"message": "Thêm vai trò thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def delete_role_with_dependencies(self, role_id):
        """Xóa vai trò và tất cả các dòng tham chiếu trong bảng mor_acl và mor_role_permission."""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Kiểm tra xem vai trò có tồn tại không
            check_sql = "SELECT id FROM mor_role WHERE id = %s"
            self.cursor.execute(check_sql, (role_id,))
            if not self.cursor.fetchone():
                return {"message": "Không tìm thấy vai trò!", "status": "error"}

            # Xóa các dòng ở bảng mor_acl liên quan đến vai trò
            sql_delete_acl = "DELETE FROM mor_acl WHERE mor_role_id = %s"
            self.cursor.execute(sql_delete_acl, (role_id,))
            self.conn.commit()  # commit ngay sau khi xóa bảng mor_acl

            # Xóa các dòng ở bảng mor_role_permission liên quan đến vai trò
            sql_delete_rp = "DELETE FROM mor_role_permission WHERE mor_role_id = %s"
            self.cursor.execute(sql_delete_rp, (role_id,))
            self.conn.commit()  # commit sau khi xóa bảng mor_role_permission

            # Cuối cùng, xóa bản ghi ở bảng mor_role
            sql_delete_role = "DELETE FROM mor_role WHERE id = %s"
            self.cursor.execute(sql_delete_role, (role_id,))
            self.conn.commit()

            return {"message": "Xóa vai trò và các tham chiếu thành công!", "status": "success"}
        except mysql.connector.Error as err:
            self.conn.rollback()
            return {"message": f"Lỗi: {err}", "status": "error"}

    def update_role(self, role_id, name, description):
        """Cập nhật thông tin vai trò"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "UPDATE mor_role SET name = %s, description = %s WHERE id = %s"
            self.cursor.execute(sql, (name, description, role_id))
            self.conn.commit()
            
            if self.cursor.rowcount == 0:
                return {"message": "Không tìm thấy vai trò!", "status": "error"}
            return {"message": "Cập nhật vai trò thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()