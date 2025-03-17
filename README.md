# User Permission Manager

Hệ thống quản lý người dùng, vai trò (role) và quyền (permission) sử dụng Flask và MySQL. Dự án này cho phép quản lý người dùng, vai trò, quyền cũng như gán quyền cho vai trò và gán vai trò cho người dùng, giúp kiểm soát truy cập vào các chức năng của ứng dụng.

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Các tính năng chính](#các-tính-năng-chính)
- [Đóng góp](#đóng-góp)
- [License](#license)
- [Liên hệ](#liên-hệ)

---

## Giới thiệu
Dự án **User Permission Manager** giúp xây dựng một hệ thống phân quyền linh hoạt cho ứng dụng web sử dụng Flask và MySQL. Qua đó, bạn có thể:
- Quản lý (thêm, sửa, xóa) thông tin người dùng.
- Quản lý các vai trò (role) và quyền (permission).
- Gán quyền cho vai trò và gán vai trò cho người dùng.
- Hỗ trợ tích hợp dễ dàng với giao diện Bootstrap.

---

## Yêu cầu hệ thống
- **Python:** 3.8 trở lên
- **MySQL:** 5.7 trở lên
- **Flask:** 2.x
- Các thư viện Python khác được liệt kê trong file `requirements.txt`

---

## Cài đặt
1. **Clone repository:**
   ```bash
   git clone https://github.com/<username>/user_permission_manager.git
   cd user_permission_manager
