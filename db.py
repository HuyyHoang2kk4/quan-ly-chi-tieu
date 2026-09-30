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



if __name__ == "__main__":
    add_expense(999999, "Ăn ", "Phở bò", "2023-10-31")
    result = get_all_expense()
    print(result)
