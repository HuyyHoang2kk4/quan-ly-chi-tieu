from src.db import get_all_expense , add_expense 
from src.category_db import get_all_categories , add_category

if __name__ == '__main__':
    print("Hệ thống bắt đầu chạy")
    add_category("Test main")
    get_all_categories = get_all_categories()
    print("Các category là  : \n " )
    print(get_all_categories)