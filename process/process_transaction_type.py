import psycopg2
from db.transaction_type_db import get_all_transaction_type, add_transaction_type, delete_transaction_type, update_transaction_type, get_transaction_type_by_id

def process_get_all_transaction_type():
    return get_all_transaction_type()

def process_add_transaction_type(transaction_type_name):
    clean_name = transaction_type_name.strip()
    if clean_name == "":
        return "Lỗi: Tên loại giao dịch không được để trống!"
        
    add_transaction_type(clean_name)
    return f"Thành công: Đã thêm loại giao dịch '{clean_name}'!"

def process_update_transaction_type(transaction_type_id, transaction_type_name):
    if get_transaction_type_by_id(transaction_type_id) is None:
        return "Lỗi: Loại giao dịch này không tồn tại!"
        
    clean_name = transaction_type_name.strip()
    if clean_name == "":
        return "Lỗi: Tên mới không được để trống!"
        
    update_transaction_type(transaction_type_id, clean_name)
    return f"Đã cập nhật tên thành '{clean_name}'!"

def process_delete_transaction_type(transaction_type_id):
    if get_transaction_type_by_id(transaction_type_id) is None:
        return "Lỗi: Không thể xóa vì loại giao dịch này không tồn tại!"
        
    try:
        delete_transaction_type(transaction_type_id)
        return "Đã xóa vĩnh viễn!"
    except psycopg2.errors.ForeignKeyViolation:
        return "Lỗi: Không thể xóa! Đang có giao dịch sử dụng loại này."
    except Exception as e:
        return f"Lỗi hệ thống: {e}"
