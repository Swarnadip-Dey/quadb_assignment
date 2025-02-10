import sqlite3
import os

DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'transactions.db')

def create_connection():
    """Creates a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_transactions_table():
    """Creates the transactions table if it doesn't exist."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_data TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Transactions table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating transactions table: {e}")
        finally:
            conn.close()
    else:
        print("Could not create transactions table, connection failed.")

def insert_transaction(transaction_data):
    """Inserts a new transaction into the transactions table."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (transaction_data)
                VALUES (?)
            """, (transaction_data,))
            conn.commit()
            print(f"Transaction added: Transaction Data={transaction_data}")
        except sqlite3.Error as e:
            print(f"Error inserting transaction: {e}")
        finally:
            conn.close()
    else:
        print("Could not insert transaction, connection failed.")

def get_all_transactions():
    """Retrieves all transactions from the transactions table."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, transaction_data FROM transactions")
            rows = cursor.fetchall()
            return [{"id": row[0], "transaction_data": row[1]} for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving transactions: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Could not retrieve transactions, connection failed.")
        return []

def delete_transaction(transaction_id):
    """Deletes a transaction from the transactions table by its ID."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            print(f"Transaction with ID {transaction_id} deleted.")
        except sqlite3.Error as e:
            print(f"Error deleting transaction: {e}")
        finally:
            conn.close()
    else:
        print("Could not delete transaction, connection failed.")

def clear_all_transactions():
    """Clears all the transaction in the database"""

    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions")
            conn.commit()
            print(f"All the Transaction are deleted")
        except sqlite3.Error as e:
            print(f"Error deleting transaction: {e}")
        finally:
            conn.close()
    else:
        print("Could not delete transaction, connection failed.")