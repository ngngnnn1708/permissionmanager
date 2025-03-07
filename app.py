from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import os
from dotenv import load_dotenv
from managers.permission_manager import PermissionManager
from managers.user_manager import UserManager
from managers.role_manager import RoleManager
from managers.role_permission_manager import RolePermissionManager
from managers.user_role_manager import UserRoleManager

# Tải biến môi trường
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ============================ TRANG CHỦ ============================
@app.route('/')
def index():
    return render_template('index.html')

# ============================ QUẢN LÝ PERMISSION ============================
@app.route('/permissions', methods=['GET'])
def get_permissions():
    pm = PermissionManager()
    permissions = pm.list_permission()

    pm.close()
    return render_template('permissions.html', permissions=permissions)

@app.route('/permissions/add', methods=['POST'])
def add_permission():
    data = request.form
    pm = PermissionManager()
    result = pm.add_permission(data['name'], data['description'])
    pm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_permissions'))

@app.route('/permissions/update', methods=['POST'])
def update_permission():
    data = request.form
    pm = PermissionManager()
    result = pm.update_permission(int(data['id']), data['name'], data['description'])
    pm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_permissions'))

@app.route('/permissions/delete/<int:permission_id>')
def delete_permission(permission_id):
    pm = PermissionManager()
    result = pm.delete_permission(permission_id)
    pm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_permissions'))

# ============================ QUẢN LÝ USER ============================
@app.route('/users', methods=['GET'])
def get_users():
    um = UserManager()
    users = um.list_users()
    um.close()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.form
    um = UserManager()
    result = um.add_user(data['name'], data['description'])
    um.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_users'))

@app.route('/users/update', methods=['POST'])
def update_user():
    data = request.form
    um = UserManager()
    result = um.update_user(int(data['id']), data['name'], data['description'])
    um.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_users'))

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    um = UserManager()
    result = um.delete_user(user_id)
    um.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_users'))

# ============================ QUẢN LÝ ROLE ============================
@app.route('/roles', methods=['GET'])
def get_roles():
    rm = RoleManager()
    roles = rm.list_roles()
    rm.close()
    return render_template('roles.html', roles=roles)

@app.route('/roles/add', methods=['POST'])
def add_role():
    data = request.form
    rm = RoleManager()
    result = rm.add_role(data['name'], data['description'])
    rm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_roles'))

@app.route('/roles/update', methods=['POST'])
def update_role():
    data = request.form
    rm = RoleManager()
    result = rm.update_role(int(data['id']), data['name'], data['description'])
    rm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_roles'))

@app.route('/roles/delete/<int:role_id>')
def delete_role(role_id):
    rm = RoleManager()
    result = rm.delete_role(role_id)
    rm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_roles'))

# ============================ GÁN PERMISSION CHO ROLE ============================
@app.route('/api/get_roles', methods=['GET'])
def api_get_roles():
    rm = RoleManager()
    roles = rm.list_roles()
    rm.close()
    return jsonify(roles)

@app.route('/api/get_permissions', methods=['GET'])
def api_get_permissions():
    pm = PermissionManager()
    permissions = pm.list_permission()
    pm.close()
    return jsonify(permissions)

@app.route('/role-permissions', methods=['GET'])
def get_role_permissions():
    rpm = RolePermissionManager()
    role_permissions = rpm.list_role_permissions()
    rpm.close()
    return render_template('role_permissions.html', role_permissions=role_permissions)

@app.route('/api/assign_permission', methods=['POST'])
def api_assign_permission():
    data = request.json  # Sử dụng request.json thay vì request.form
    if not data or 'role_id' not in data or 'permission_id' not in data:
        return jsonify({"message": "Thiếu dữ liệu role_id hoặc permission_id"}), 400

    rpm = RolePermissionManager()
    result = rpm.assign_permission_to_role(int(data['role_id']), int(data['permission_id']))
    rpm.close()
    
    return jsonify(result), 200

@app.route('/role-permissions/assign', methods=['POST'])
def assign_permission_to_role():
    data = request.form
    rpm = RolePermissionManager()
    result = rpm.assign_permission_to_role(int(data['role_id']), int(data['permission_id']))
    rpm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_role_permissions'))

@app.route('/role-permissions/remove', methods=['POST'])
def remove_permission_from_role():
    data = request.form
    rpm = RolePermissionManager()
    result = rpm.remove_permission_from_role(int(data['role_id']), int(data['permission_id']))
    rpm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_role_permissions'))

# ============================ GÁN ROLE CHO USER ============================
@app.route('/user-roles', methods=['GET'])
def get_user_roles():
    urm = UserRoleManager()
    user_roles = urm.list_user_roles()
    urm.close()
    return render_template('user_roles.html', user_roles=user_roles)

@app.route('/user-roles/assign', methods=['POST'])
def assign_role_to_user():
    data = request.form
    urm = UserRoleManager()
    result = urm.assign_role(int(data['user_id']), int(data['role_id']))
    urm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_user_roles'))

@app.route('/user-roles/remove', methods=['POST'])
def remove_role_from_user():
    data = request.form
    urm = UserRoleManager()
    result = urm.remove_role(int(data['user_id']), int(data['role_id']))
    urm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_user_roles'))

if __name__ == '__main__':
    app.run(debug=True)
