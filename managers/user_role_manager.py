import mysql.connector
import os
from dotenv import load_dotenv

class UserRoleManager:
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

    def list_user_roles(self):
        """
        Lấy tất cả các dòng trong bảng mor_acl, trả về danh sách 
        [{'mor_user_id': x, 'mor_role_id': y}, ...]
        """
        if not self.conn:
            return []
        try:
            sql = "SELECT mor_user_id, mor_role_id FROM mor_acl"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data if data else []
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
            return []

    def assign_role_to_user(self, user_id, role_id):
        """Gán một vai trò cho người dùng (thêm dòng vào bảng mor_acl)"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "INSERT INTO mor_acl (mor_user_id, mor_role_id) VALUES (%s, %s)"
            self.cursor.execute(sql, (user_id, role_id))
            self.conn.commit()
            return {"message": "Gán vai trò thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def remove_role_from_user(self, user_id, role_id):
        """Xóa vai trò khỏi người dùng (xóa dòng trong bảng mor_acl)"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "DELETE FROM mor_acl WHERE mor_user_id = %s AND mor_role_id = %s"
            self.cursor.execute(sql, (user_id, role_id))
            self.conn.commit()
            
            if self.cursor.rowcount == 0:
                return {"message": "Không tìm thấy vai trò này cho người dùng!", "status": "error"}
            return {"message": "Xóa vai trò thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def get_roles_by_user(self, user_id):
        """Lấy danh sách vai trò của một người dùng cụ thể"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = """
                SELECT r.id, r.name, r.description
                FROM mor_role r
                JOIN mor_acl a ON r.id = a.mor_role_id
                WHERE a.mor_user_id = %s
            """
            self.cursor.execute(sql, (user_id,))
            data = self.cursor.fetchall()
            return data if data else []
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()