from src.db import get_connection

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


def add_category(name_category):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """
        INSERT INTO categories (name_category) 
        VALUES (%s)

    """
    cur.execute(sql_query, (name_category,))
    conn.commit()
    cur.close()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        DELETE FROM categories where id = %s 
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
        SET name_category = %s
        WHERE id = %s 
    """
    cur.execute(sql_query, (category_name ,category_id ))
    conn.commit()
    conn.close()