import os
import psycopg

from dotenv import load_dotenv

load_dotenv()

def get_connection():
    my_host = os.getenv("DB_HOST")
    my_port = os.getenv("DB_PORT")
    my_db = os.getenv("DB_NAME")
    my_user = os.getenv("DB_USER")
    my_password = os.getenv("DB_PASSWORD")

    conn = psycopg.connect(
        host=my_host,
        port=my_port,
        dbname=my_db,
        user=my_user,
        password=my_password
    )
    return conn 


def add_transaction(amount, category_id, note, spent_on , transaction_type_id):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """
        INSERT INTO transactions (amount, category_id, note, spent_on , transaction_type_id) 
        VALUES (%s, %s, %s, %s , %s)

    """
    cur.execute(sql_query, (amount, category_id, note, spent_on , transaction_type_id))
    conn.commit()
    cur.close()
    conn.close()

def get_all_transaction():
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """
        SELECT transactions.transaction_id , transactions.amount , categories.name_category , transactions.note , transactions.spent_on , transaction_type.transaction_type_name
        FROM transactions
        JOIN categories ON transactions.category_id = categories.category_id
        JOIN transaction_type ON transactions.transaction_type_id = transaction_type.transaction_type_id ;
    """
    cur.execute(sql_query)
    transactions_list = cur.fetchall()
    cur.close()
    conn.close()
    return transactions_list

def delete_transaction(delete_transaction_id):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        DELETE FROM transactions where transaction_id = %s 
    """
    cur.execute(sql_query , (delete_transaction_id,))
    conn.commit()
    conn.close()

def update_transaction(transaction_id ,amount, category_id, note, spent_on , transaction_type_id):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        UPDATE transactions
        SET amount = %s , category_id = %s , note = %s , spent_on=%s , transaction_type_id=%s
        WHERE transaction_id = %s 
    """
    cur.execute(sql_query, (amount, category_id, note, spent_on,transaction_type_id,transaction_id,))
    conn.commit()
    conn.close()

def get_transaction_by_id (transaction_id) :
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        SELECT * FROM transactions WHERE transaction_id = %s
    """
    cur.execute(sql_query , (transaction_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


