from src.transactions_db import get_connection

def get_all_categories() :
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
    SELECT * FROM categories
    """
    cur.execute(sql_query)
    categories_list = cur.fetchall()
    cur.close()
    conn.close()
    return categories_list


def add_category(category_name):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """
        INSERT INTO categories (category_name) 
        VALUES (%s)

    """
    cur.execute(sql_query, (category_name,))
    conn.commit()
    cur.close()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        DELETE FROM categories where category_id = %s 
    """
    cur.execute(sql_query , (category_id,))
    conn.commit()
    cur.close()
    conn.close()

def update_category(category_id , category_name):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        UPDATE categories
        SET category_name = %s
        WHERE category_id = %s 
    """
    cur.execute(sql_query, (category_name ,category_id ))
    conn.commit()
    conn.close()