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

@app.route('/permission/update', methods=['POST'])
def update_permission():
    data = request.form
    pm = PermissionManager()
    result = pm.update_permission(int(data['id']), data['name'], data['description'])
    pm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_permissions'))

@app.route('/permissions/force-delete/<int:permission_id>')
def force_delete_permission(permission_id):
    pm = PermissionManager()
    result = pm.delete_permission_with_dependencies(permission_id)
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

@app.route('/users/force-delete/<int:user_id>')
def force_delete_user(user_id):
    um = UserManager()
    result = um.delete_user_with_dependencies(user_id)
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

@app.route('/roles/force-delete/<int:role_id>')
def force_delete_role(role_id):
    rm = RoleManager()
    result = rm.delete_role_with_dependencies(role_id)
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
    # Khởi tạo các manager
    rpm = RolePermissionManager()
    rm = RoleManager()
    pm = PermissionManager()

    # Lấy dữ liệu thô
    role_permissions_raw = rpm.list_role_permissions()   # [{mor_role_id, mor_permission_id}, ...]
    roles = rm.list_roles()                               # [{id, name, description}, ...]
    permissions = pm.list_permission()                    # [{id, name, description}, ...]

    # Đóng kết nối
    rpm.close()
    rm.close()
    pm.close()

    # Tạo dict tra cứu vai trò: key = role_id, value = {id, name, permissions: []}
    role_permissions_dict = {}
    for r in roles:
        role_permissions_dict[r['id']] = {
            "id": r['id'],
            "name": r['name'],
            "permissions": []  # sẽ chứa các quyền
        }

    # Tạo dict tra cứu quyền: key = permission_id, value = {id, name, ...}
    perms_dict = {p['id']: p for p in permissions}

    # Ghép danh sách quyền cho mỗi role
    for item in role_permissions_raw:
        role_id = item['mor_role_id']
        perm_id = item['mor_permission_id']

        # Nếu role_id và perm_id tồn tại, thêm vào danh sách
        if role_id in role_permissions_dict and perm_id in perms_dict:
            role_permissions_dict[role_id]['permissions'].append({
                "id": perm_id,
                "name": perms_dict[perm_id]['name']
            })

    # role_permissions_list là mảng final để truyền xuống template
    role_permissions_list = list(role_permissions_dict.values())

    # Render template, truyền 3 biến chính:
    # - role_permissions_list: Dữ liệu bảng "Danh sách Quyền theo Vai Trò"
    # - roles: Dữ liệu dropdown chọn vai trò
    # - permissions: Dữ liệu dropdown chọn quyền
    return render_template(
        'role_permissions.html',
        role_permissions_list=role_permissions_list,
        roles=roles,
        permissions=permissions
    )

@app.route('/role-permissions/assign', methods=['POST'])
def assign_permission_to_role():
    data = request.form
    role_id = int(data['role_id'])
    permission_id = int(data['permission_id'])

    rpm = RolePermissionManager()
    result = rpm.assign_permission_to_role(role_id, permission_id)
    rpm.close()

    flash(result['message'], result['status'])
    return redirect(url_for('get_role_permissions'))

@app.route('/role-permissions/remove', methods=['POST'])
def remove_permission_from_role():
    data = request.form
    role_id = int(data['role_id'])
    permission_id = int(data['permission_id'])

    rpm = RolePermissionManager()
    result = rpm.remove_permission_from_role(role_id, permission_id)
    rpm.close()

    flash(result['message'], result['status'])
    return redirect(url_for('get_role_permissions'))


# ============================ GÁN ROLE CHO USER ============================
@app.route('/user-roles', methods=['GET'])
def get_user_roles():
    """
    Lấy danh sách user, danh sách role, và danh sách gán (user->role),
    sau đó gộp chúng lại để hiển thị ở user_roles.html
    """
    um = UserManager()
    rm = RoleManager()
    urm = UserRoleManager()

    # Lấy dữ liệu từ DB
    all_users = um.list_users()           # [{id, name, ...}, ...]
    all_roles = rm.list_roles()           # [{id, name, ...}, ...]
    user_roles_raw = urm.list_user_roles()# [{mor_user_id, mor_role_id}, ...]

    um.close()
    rm.close()
    urm.close()

    # Tạo dict: key = user_id, value = {id, name, roles: []}
    user_roles_dict = {}
    for u in all_users:
        user_roles_dict[u['id']] = {
            'id': u['id'],
            'name': u['name'],
            'roles': []
        }

    # Tạo dict tra cứu role theo role_id
    roles_dict = {r['id']: r for r in all_roles}

    # Gắn các role vào user tương ứng
    for item in user_roles_raw:
        user_id = item['mor_user_id']
        role_id = item['mor_role_id']
        if user_id in user_roles_dict and role_id in roles_dict:
            user_roles_dict[user_id]['roles'].append({
                'id': role_id,
                'name': roles_dict[role_id]['name']
            })

    # user_roles_list là danh sách cuối cùng để render
    user_roles_list = list(user_roles_dict.values())

    # Truyền thêm all_users và all_roles để hiển thị dropdown
    return render_template(
        'user_roles.html',
        user_roles=user_roles_list,
        users=all_users,
        roles=all_roles
    )

@app.route('/user-roles/assign', methods=['POST'])
def assign_role_to_user():
    data = request.form
    urm = UserRoleManager()
    # Gọi phương thức assign_role_to_user trong user_role_manager.py
    result = urm.assign_role_to_user(int(data['user_id']), int(data['role_id']))
    urm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_user_roles'))

@app.route('/user-roles/remove', methods=['POST'])
def remove_role_from_user():
    data = request.form
    urm = UserRoleManager()
    # Gọi phương thức remove_role_from_user trong user_role_manager.py
    result = urm.remove_role_from_user(int(data['user_id']), int(data['role_id']))
    urm.close()
    flash(result['message'], result['status'])
    return redirect(url_for('get_user_roles'))

if __name__ == '__main__':
    app.run(debug=True)
