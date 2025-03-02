from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

# Kết nối MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="ngocnam170898@",
        database="user_management"
    )

# Route hiển thị danh sách quyền
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mor_permission")
    permissions = cursor.fetchall()
    conn.close()
    return render_template("index.html", permissions=permissions)

# Route thêm quyền
@app.route('/add', methods=['POST'])
def add_permission():
    permission_id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO mor_permission (ID, Name, Description) VALUES (%s, %s, %s)",
                       (permission_id, name, description))
        conn.commit()
        flash("Thêm quyền thành công!", "success")
    except mysql.connector.Error as err:
        flash(f"Lỗi: {err}", "danger")
    conn.close()
    return redirect(url_for('index'))

# Route cập nhật quyền
@app.route('/update', methods=['POST'])
def update_permission():
    permission_id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE mor_permission SET Name=%s, Description=%s WHERE ID=%s",
                   (name, description, permission_id))
    conn.commit()
    conn.close()
    
    flash("Cập nhật quyền thành công!", "success")
    return redirect(url_for('index'))

# Route xóa quyền
@app.route('/delete/<int:permission_id>')
def delete_permission(permission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mor_permission WHERE ID=%s", (permission_id,))
    conn.commit()
    conn.close()

    flash("Xóa quyền thành công!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)