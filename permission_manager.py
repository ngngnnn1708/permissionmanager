import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

class PermissionManager:
    def __init__(self, host=None, user=None, password=None, database=None):
        """Khởi tạo kết nối MySQL"""
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
    
    def add_permission(self, name, description):
        """Thêm quyền mới vào bảng mor_permission với ID tự động tăng"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            sql = "INSERT INTO mor_permission (Name, Description) VALUES (%s, %s)"
            self.cursor.execute(sql, (name, description))
            self.conn.commit()
            return {"message": "Thêm quyền thành công!", "status": "success"}
        except mysql.connector.Error as err:
            return {"message": f"Lỗi: {err}", "status": "error"}
    
    def reset_auto_increment(self):
        """Đặt lại AUTO_INCREMENT để ID tăng dần theo thứ tự không bị nhảy"""
        try:
            # Lấy ID lớn nhất hiện tại
            self.cursor.execute("SELECT MAX(ID) as max_id FROM mor_permission")
            result = self.cursor.fetchone()
            max_id = result['max_id'] if result and result['max_id'] else 0

            # Đặt lại giá trị AUTO_INCREMENT là max_id + 1
            self.cursor.execute(f"ALTER TABLE mor_permission AUTO_INCREMENT = {max_id + 1}")
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Lỗi khi đặt lại AUTO_INCREMENT: {err}")

    def delete_permission(self, permission_id):
        """Xóa quyền trong bảng mor_permission"""
        if not self.conn:
            return {"message": "Lỗi kết nối CSDL!", "status": "error"}
        try:
            # Xóa quyền
            sql = "DELETE FROM mor_permission WHERE ID = %s"
            self.cursor.execute(sql, (permission_id,))
            self.conn.commit()
            
            if self.cursor.rowcount == 0:
                return {"message": "Không tìm thấy quyền!", "status": "error"}
            
            # Đặt lại AUTO_INCREMENT sau khi xóa
            self.reset_auto_increment()
            
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