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


def add_expense(amount, category, note, spent_on):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """
        INSERT INTO expenses (amount, category, note, spent_on) 
        VALUES (%s, %s, %s, %s)

    """
    cur.execute(sql_query, (amount, category, note, spent_on))
    conn.commit()

    # cur.close()
    conn.close()

def get_all_expense():
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """
        SELECT * FROM expenses
    """
    cur.execute(sql_query)
    expense_list = cur.fetchall()
    cur.close()
    conn.close()
    
    return expense_list

def delete_expense(delete_id):
    conn = get_connection()
    cur = conn.cursor()
    sql_query = """ 
        DELETE FROM expenses where id = %s 
    """
    cur.execute(sql_query , (delete_id,))
    conn.commit()
    conn.close()

def update_expense(expense_id ,amount, category, note, spent_on):
    conn = get_connection()

    cur = conn.cursor()

    sql_query = """ 
        UPDATE expenses
        SET amount = %s , category = %s , note = %s , spent_on=%s
        WHERE id = %s 
    """

    cur.execute(sql_query, (amount, category, note, spent_on,expense_id,))

    conn.commit()

    conn.close()



if __name__ == "__main__":
    # print(result)

    update_expense(2 , 9999999 ,"UPDATE ", "UPDATE" , "2026-10-10")
    result = get_all_expense()
    print(result)

