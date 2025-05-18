# Note App

## Tổng Quan

Note App là một ứng dụng quản lý ghi chú đơn giản, được phát triển với Flask (Backend) và HTML/CSS (Frontend). Ứng dụng cho phép tạo, đọc, cập nhật và xóa ghi chú, phân loại chúng bằng danh mục và thẻ.

## Tính Năng Chính

- **Quản lý ghi chú**: Tạo, đọc, cập nhật và xóa ghi chú.
- **Danh mục**: Phân loại ghi chú theo danh mục.
- **Thẻ (Tags)**: Gắn thẻ cho ghi chú để dễ tìm kiếm.
- **Tìm kiếm**: Tìm kiếm ghi chú bằng từ khóa.
- **Lọc**: Lọc ghi chú theo danh mục hoặc thẻ.

## Công Nghệ Sử Dụng

### Backend

- **Flask**: Framework web Python nhẹ và linh hoạt.
- **SQLite**: Hệ quản trị cơ sở dữ liệu nhẹ.
- **Flask-CORS**: Hỗ trợ Cross-Origin Resource Sharing.

### Frontend

- **HTML/CSS**: Cấu trúc và định dạng giao diện.
- **Bootstrap**: Framework CSS cho giao diện responsive.

## Cài Đặt và Chạy Ứng Dụng

### Yêu Cầu

- Python 3.7+
- pip
- Visual Studio Code với extension Live Server (khuyến nghị)

### Các Bước

1. Clone dự án:

   ```bash
   git clone <repository-url>
   cd note_app
   ```

2. Cài đặt thư viện:

   ```bash
   pip install flask flask-cors
   ```

3. Chạy backend:

   ```bash
   python app.py
   ```

   - Backend sẽ chạy trên `http://127.0.0.1:5000`.

5. Chạy frontend:

   - Mở `index.html` trong VS Code.
   - Nhấn **Go Live** (yêu cầu extension Live Server).
   - Frontend sẽ chạy trên `http://127.0.0.1:5500/index.html`.

6. Truy cập:

   - Mở trình duyệt và vào `http://127.0.0.1:5500/index.html`.

## Cấu Trúc Cơ Sở Dữ Liệu

Ứng dụng sử dụng SQLite với 5 bảng:

1. **notes**: Lưu thông tin ghi chú.

   - `id`: Khóa chính, tự tăng.
   - `title`: Tiêu đề (bắt buộc).
   - `content`: Nội dung.
   - `created_at`: Thời gian tạo.

2. **categories**: Lưu danh mục.

   - `id`: Khóa chính, tự tăng.
   - `name`: Tên danh mục (duy nhất).

3. **tags**: Lưu thẻ.

   - `id`: Khóa chính, tự tăng.
   - `name`: Tên thẻ (duy nhất).

4. **note_categories**: Quan hệ nhiều-nhiều giữa notes và categories.

   - `note_id`: Khóa ngoại tham chiếu bảng notes.
   - `category_id`: Khóa ngoại tham chiếu bảng categories.

5. **note_tags**: Quan hệ nhiều-nhiều giữa notes và tags.

   - `note_id`: Khóa ngoại tham chiếu bảng notes.
   - `tag_id`: Khóa ngoại tham chiếu bảng tags.

### Lợi ích của SQLite 

- **Nhẹ và Dễ Sử Dụng**: SQLite không yêu cầu cấu hình phức tạp hay máy chủ riêng, phù hợp cho ứng dụng nhỏ như Note App. 
- **Hỗ Trợ Quan Hệ Dữ Liệu**: Với các bảng như `note_categories` và `note_tags`, SQLite cho phép quản lý quan hệ nhiều-nhiều giữa ghi chú, danh mục và thẻ một cách hiệu quả, sử dụng khóa ngoại (`FOREIGN KEY`) để đảm bảo tính toàn vẹn dữ liệu.
- **Tích Hợp Tốt với Python**: SQLite có thư viện tích hợp sẵn trong Python (module `sqlite3`), không cần cài đặt thêm, giúp tiết kiệm thời gian phát triển. File `init_db.py` sử dụng module này để tạo bảng và thêm dữ liệu mẫu.
- **Phù Hợp cho Ứng Dụng Đơn Lẻ**: Vì Note App hiện tại được thiết kế cho một người dùng hoặc một phiên bản cục bộ, SQLite đáp ứng tốt nhu cầu lưu trữ dữ liệu mà không cần quy mô lớn như MySQL hay PostgreSQL.

SQLite đóng vai trò quan trọng trong việc lưu trữ và quản lý dữ liệu, đảm bảo rằng các thao tác CRUD (tạo, đọc, cập nhật, xóa) thông qua API của Flask hoạt động trơn tru. 
