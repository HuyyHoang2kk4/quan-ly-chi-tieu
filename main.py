from process.process_category import process_get_all_categories , process_add_category , process_update_category , process_delete_category

if __name__ == '__main__':
    print("Hệ thống bắt đầu chạy")
    # process_add_category("Hoang")
    process_update_category(4,"Hoang update")
    # process_delete_category(6)
    print(process_get_all_categories())

