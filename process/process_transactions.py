from db.transactions_db import add_transaction , get_all_transaction  ,delete_transaction , update_transaction ,  get_transaction_by_id
import psycopg2

def process_add_transaction(amount_str, category_id, note, spent_on , transaction_type_id) :
    try :
        amount = float(amount_str)

        if amount < 0:
            return "Lỗi : Số tiền phải >0"

        if category_id == "" or category_id is None :
            return "Lỗi : Bạn chưa chọn Category "

        if spent_on == "" or  spent_on is None :
            return "Lỗi : Bạn chưa chọn ngày giao dịch"

        if transaction_type_id == "" or transaction_type_id is None :
            return "Bạn chưa chọn loại giao dịch thu chi"  
        
        add_transaction(amount ,category_id, note, spent_on , transaction_type_id)
        return "Thành công : Đã lưu giao dịch thành công "

    except ValueError:
        return "Lỗi : Bạn phải nhập số tiền là con số"

    except psycopg2.errors.InvalidDatetimeFormat :
        return "Lỗi : Bạn nhập ko đúng ngày tháng"

    except Exception as e : 
        return f"Lỗi thêm transaction : {e}" 

def process_get_all_transactions():
    try :
        return get_all_transaction()
    except Exception as e :
        return "Lỗi Get giao dịch : {e}"

def process_delete_transaction(transaction_id):

    if get_transaction_by_id(transaction_id) is None:
        return "Lỗi : Không trùng với ID transaction"

    try :
        delete_transaction(transaction_id)
        return "Đã xoá thành công transaction có id {transaction_id}"

    except Exception as e :
        return f"Lỗi xoá transaction : {e}"

def process_update_trainsaction(transaction_id,amount_str, category_id, note, spent_on, transaction_type_id) : 
    if get_transaction_by_id(transaction_id) is None:
        return "Lỗi : Không trùng với ID transaction"

    try :
        amount = float(amount_str)

        if amount < 0:
            return "Lỗi : Số tiền phải >0"
        update_transaction(transaction_id, amount, category_id, note, spent_on, transaction_type_id)
        
        return "Đã update transaction thành công"


    except ValueError:
        return "Lỗi : Bạn phải nhập số tiền là con số"

    except Exception as e :
        return "Lỗi : Update transaction {e}"