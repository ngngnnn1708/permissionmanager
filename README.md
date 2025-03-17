# User Permission Manager

## Giới thiệu
User Permission Manager là một hệ thống quản lý người dùng, vai trò và quyền sử dụng Flask và MySQL. Dự án này cho phép bạn:
- Quản lý (thêm, sửa, xóa) người dùng
- Quản lý vai trò và quyền
- Gán quyền cho vai trò và gán vai trò cho người dùng

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Các tính năng chính](#các-tính-năng-chính)
- [Đóng góp](#đóng-góp)
- [License](#license)
- [Liên hệ](#liên-hệ)

## Yêu cầu hệ thống
- Python 3.8 trở lên
- MySQL 5.7 trở lên
- Flask 2.x
- Các gói Python được liệt kê trong file `requirements.txt`

## Cài đặt
1. Clone repository:
   ```bash
   git clone https://github.com/<username>/<repository>.git
   cd <repository>
   ```
2. Tạo virtual environment và cài đặt các gói cần thiết:
   ```bash
   python -m venv venv
   source venv/bin/activate  # hoặc venv\Scripts\activate trên Windows
   pip install -r requirements.txt
   ```
3. Tạo file **.env** với nội dung:
   ```env
   SECRET_KEY=your_secret_key
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=user_management
   ```
4. Tạo database **user_management** trên MySQL.

## Hướng dẫn sử dụng
1. Chạy ứng dụng:
   ```bash
   python app.py
   ```
2. Mở trình duyệt và truy cập [http://127.0.0.1:5000](http://127.0.0.1:5000).
3. Sử dụng các chức năng:
   - **Quản lý Người dùng:** `/users`
   - **Quản lý Vai trò:** `/roles`
   - **Quản lý Quyền:** `/permissions`
   - **Gán quyền cho vai trò:** `/role-permissions`
   - **Gán vai trò cho người dùng:** `/user-roles`

## Cấu trúc dự án
user_permission_manager/
├── managers/
│   ├── user_manager.py
│   ├── role_manager.py
│   ├── permission_manager.py
│   ├── user_role_manager.py
│   └── role_permission_manager.py
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── users.html
│   ├── roles.html
│   ├── permissions.html
│   ├── role_permissions.html
│   └── user_roles.html
├── .env
├── app.py
├── requirements.txt
└── README.md

## Các tính năng chính
- Quản lý Người dùng: Thêm, sửa, xóa người dùng và xử lý các ràng buộc khóa ngoại.
- Quản lý Vai trò: Thêm, sửa, xóa vai trò, bao gồm xóa vai trò kèm theo các tham chiếu.
- Quản lý Quyền: Thêm, sửa, xóa quyền và gán quyền cho vai trò.
- Gán vai trò cho người dùng và gán quyền cho vai trò qua giao diện web.

## Đóng góp
Nếu bạn muốn đóng góp vào dự án này:
1. Fork repository.
2. Tạo branch mới cho tính năng hoặc fix lỗi.
3. Commit thay đổi và push lên branch.
4. Tạo Pull Request để trao đổi và hợp nhất thay đổi.

Vui lòng báo lỗi hoặc đề xuất cải tiến bằng cách mở [Issue](https://github.com/ngngnnn1708/permissionmanager).

## Liên hệ
- **Tác giả:** [Nam Nguyễn](https://github.com/ngngnnn1708)
- **Email:** nguyenngocnam1708@gmail.com
- **Dự án trên GitHub:** [https://github.com/ngngnnn1708/permissionmanager](https://github.com/ngngnnn1708/permissionmanager)
