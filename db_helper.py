import logging

import mysql.connector
from contextlib import contextmanager
from .logging_setup import setup_logger


logger = logging.getLogger('db_helper')

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("server.log")

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)





@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    try:
        with get_db_cursor(commit=True) as cursor:
            # Convert date object to string if needed
            if hasattr(expense_date, 'isoformat'):
                expense_date = expense_date.isoformat()
            
            logger.info(f"Executing INSERT with params: {expense_date}, {amount}, {category}, {notes}")
            cursor.execute(
                "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                (str(expense_date), float(amount), str(category), str(notes))
            )
            logger.info(f"Insert successful. Rows affected: {cursor.rowcount}")
    except Exception as e:
        logger.error(f"Error inserting expense: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)   
