from src.transactions_db import get_all_expense , add_expense 
from src.category_db import get_all_categories , add_category

if __name__ == '__main__':
    print("Hệ thống bắt đầu chạy")
    # add_category("Test main")
    get_all_categories = get_all_categories()
    print("Các category là  : \n " )
    print(get_all_categories)
    #-------------------
    add_expense(9999 , 2 , "test note main " , "2025-12-12")
    
    chi_tieu = get_all_expense()
    print("Các khoản chi tiêu là: \n")
    print(chi_tieu)

