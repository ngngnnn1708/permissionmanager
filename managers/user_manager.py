import mysql.connector
import os
from dotenv import load_dotenv

class UserManager:
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

    def list_users(self):
        """Liệt kê danh sách tất cả người dùng"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "SELECT id, name, description FROM mor_user"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data if data else []
        except mysql.connector.Error as err:
            return {"message": f"Lỗi {err}", "status": "error"}

    def add_user(self, name, description):
        """Thêm người dùng mới"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Kiểm tra trùng lặp
            check_sql = "SELECT COUNT(*) as count FROM mor_user WHERE name = %s"
            self.cursor.execute(check_sql, (name,))
            if self.cursor.fetchone()["count"] > 0:
                return {"message": "Người dùng đã tồn tại!", "status": "error"}

            sql = "INSERT INTO mor_user (name, description) VALUES (%s, %s)"
            self.cursor.execute(sql, (name, description))
            self.conn.commit()
            return {"message": "Thêm người dùng thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def update_user(self, user_id, name, description):
        """Cập nhật thông tin người dùng"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Kiểm tra user có tồn tại không
            check_sql = "SELECT id FROM mor_user WHERE id = %s"
            self.cursor.execute(check_sql, (user_id,))
            if not self.cursor.fetchone():
                return {"message": "Không tìm thấy người dùng!", "status": "error"}

            sql = "UPDATE mor_user SET name = %s, description = %s WHERE id = %s"
            self.cursor.execute(sql, (name, description, user_id))
            self.conn.commit()
            return {"message": "Cập nhật người dùng thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}

    def delete_user_with_dependencies(self, user_id):
        """Xóa người dùng và tất cả các dòng tham chiếu trong bảng mor_acl."""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Kiểm tra xem người dùng có tồn tại không
            check_sql = "SELECT id FROM mor_user WHERE id = %s"
            self.cursor.execute(check_sql, (user_id,))
            if not self.cursor.fetchone():
                return {"message": "Không tìm thấy người dùng!", "status": "error"}

            # Xóa các dòng trong bảng mor_acl liên quan đến người dùng
            sql_delete_refs = "DELETE FROM mor_acl WHERE mor_user_id = %s"
            self.cursor.execute(sql_delete_refs, (user_id,))
            self.conn.commit()  # commit ngay sau khi xóa các dòng ở bảng con

            # Sau đó xóa bản ghi người dùng trong bảng mor_user
            sql_delete_user = "DELETE FROM mor_user WHERE id = %s"
            self.cursor.execute(sql_delete_user, (user_id,))
            self.conn.commit()

            return {"message": "Xóa người dùng và các tham chiếu thành công!", "status": "success"}
        except mysql.connector.Error as err:
            self.conn.rollback()
            return {"message": f"Lỗi: {err}", "status": "error"}

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
