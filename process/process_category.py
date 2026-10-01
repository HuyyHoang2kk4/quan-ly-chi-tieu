import psycopg2
from db.category_db import get_all_categories, add_category, delete_category, update_category, get_category_by_id

def process_get_all_categories():
    return get_all_categories()

def process_add_category(category_name):
    clean_name = category_name.strip()
    if clean_name == "":
        return "Lỗi: Tên danh mục không được để trống!"
    add_category(clean_name)
    return f"Thành công: Đã thêm danh mục '{clean_name}'!"

def process_update_category(category_id, category_name):
    if get_category_by_id(category_id) is None:
        return "Lỗi: Danh mục này không tồn tại!"
    clean_name = category_name.strip()
    if clean_name == "":
        return "Lỗi: Tên danh mục mới không được để trống!"
    update_category(category_id, clean_name)
    return f"Đã cập nhật tên danh mục thành '{clean_name}'!"

def process_delete_category(category_id):
    if get_category_by_id(category_id) is None:
        return "Lỗi: Không thể xóa vì danh mục không tồn tại!"
    try:
        delete_category(category_id)
        return "Đã xóa danh mục vĩnh viễn!"
    except psycopg2.errors.ForeignKeyViolation:
        return "Lỗi: Không thể xóa! Đang có giao dịch sử dụng danh mục này."
    except Exception as e:
        return f"Lỗi hệ thống: {e}"
