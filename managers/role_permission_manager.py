import mysql.connector
import os
from dotenv import load_dotenv

class RolePermissionManager:
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

    def list_role_permissions(self):
        """Liệt kê danh sách quyền theo vai trò"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "SELECT role_id, permission_id FROM mor_role_permission"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data if data else []
        except mysql.connector.Error as err:
            return {"message": f"Lỗi {err}", "status": "error"}

    def assign_permission_to_role(self, role_id, permission_id):
        """Gán một quyền cho một vai trò"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "INSERT INTO mor_role_permission (mor_role_id, mor_permission_id) VALUES (%s, %s)"
            self.cursor.execute(sql, (role_id, permission_id))
            self.conn.commit()
            return {"message": "Gán quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def remove_permission_from_role(self, role_id, permission_id):
        """Xóa quyền khỏi vai trò"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "DELETE FROM mor_role_permission WHERE mor_role_id = %s AND mor_permission_id = %s"
            self.cursor.execute(sql, (role_id, permission_id))
            self.conn.commit()
            
            if self.cursor.rowcount == 0:
                return {"message": "Không tìm thấy quyền này trong vai trò!", "status": "error"}
            return {"message": "Xóa quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def get_permissions_by_role(self, role_id):
        """Lấy danh sách quyền theo vai trò"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = """
                SELECT p.id, p.name, p.description
                FROM mor_permission p
                JOIN mor_role_permission rp ON p.id = rp.mor_permission_id
                WHERE rp.mor_role_id = %s
            """
            self.cursor.execute(sql, (role_id,))
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
