from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from permission_manager import PermissionManager

#Tải biến môi trường từ file .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Route hiển thị danh sách quyền
@app.route('/')
def index():
    pm = PermissionManager()
    permissions = pm.list_permission()
    if isinstance(permissions, dict) and permissions.get('status') == 'error':
        flash(permissions['message'], "danger")
        permissions = []
    else:
        # Chuyển DataFrame thành list of dictionaries
        permissions = permissions.to_dict('records') if not isinstance(permissions, list) else permissions
    pm.close()
    return render_template("index.html", permissions=permissions)

# Route thêm quyền
@app.route('/add', methods=['POST'])
def add_permission():
    try:
        name = request.form['name']
        description = request.form['description']
    
        pm = PermissionManager()
        result = pm.add_permission(name, description)
        pm.close()

        flash(result['message'], result['status'])
    except Exception as e:
        flash(f"Lỗi: {str(e)}", "danger")

    return redirect(url_for('index'))

# Route cập nhật quyền
@app.route('/update', methods=['POST'])
def update_permission():
    try:
        permission_id = int(request.form['id'])
        name = request.form['name']
        description = request.form['description']
    
        pm = PermissionManager()
        result = pm.update_permission(permission_id, name, description)
        pm.close()

        flash(result['message'], result['status'])
    except ValueError:
        flash("Lỗi: ID không hợp lệ!", "danger")
    
    return redirect(url_for('index'))

# Route xóa quyền
@app.route('/delete/<int:permission_id>')
def delete_permission(permission_id):
    pm = PermissionManager()
    result = pm.delete_permission(permission_id)
    pm.close()
    
    flash(result['message'], result['status'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)