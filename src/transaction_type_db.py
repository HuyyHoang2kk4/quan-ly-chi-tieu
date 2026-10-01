from src.transactions_db import get_connection

def get_all_transaction_type() :
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
    SELECT * FROM transaction_type
    """
    cur.execute(sql_query)
    transaction_type_list = cur.fetchall()
    cur.close()
    conn.close()
    return transaction_type_list


def add_transaction_type(transaction_type_name):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """
        INSERT INTO transaction_type (transaction_type_name) 
        VALUES (%s)

    """
    cur.execute(sql_query, (transaction_type_name,))
    conn.commit()
    cur.close()
    conn.close()

def delete_transaction_type(transaction_type_id):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        DELETE FROM transaction_type where transaction_type_id = %s 
    """
    cur.execute(sql_query , (transaction_type_id,))
    conn.commit()
    cur.close()
    conn.close()

def update_transaction_type(transaction_type_id , transaction_type_name):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        UPDATE transaction_type
        SET transaction_type_name = %s
        WHERE transaction_type_id = %s 
    """
    cur.execute(sql_query, (transaction_type_name ,transaction_type_id ))
    conn.commit()
    conn.close()