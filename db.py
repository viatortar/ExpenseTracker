import sqlite3

class Database:
    @staticmethod
    def connect_to_database():
        conn = sqlite3.connect('tabungan.db')
        cursor = conn.cursor()

        # Create Transactions table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                amount REAL,
                description TEXT
            )
        ''')
        
        conn.commit()
        return conn

    @staticmethod
    def add_transaction(conn, values):
        cursor = conn.cursor()
        type_choice, amount, description = values

        # Convert amount to float and adjust the sign based on the transaction type
        try:
            amount = float(amount)
        except ValueError:
            raise ValueError("Invalid amount. Please enter a valid number.")
        
        if type_choice == 'expense':
            amount = -abs(amount)  # Ensure that the amount is stored as a negative value for expenses
        else:
            amount = abs(amount)  # Ensure that the amount is stored as a positive value for income

        cursor.execute('''
            INSERT INTO transactions (type, amount, description) VALUES (?, ?, ?)
        ''', (type_choice, amount, description))
        conn.commit()

    @staticmethod
    def read_database(conn):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions')
        return cursor.fetchall()

    @staticmethod
    def edit_transaction(conn, values):
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions SET amount=?, description=? WHERE id=?
        ''', values)
        conn.commit()

    @staticmethod
    def delete_transaction(conn, transaction_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id=?', (transaction_id,))
        conn.commit()

    @staticmethod
    def total_balance(conn):
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(amount) FROM transactions')
        result = cursor.fetchone()
        return result[0] if result[0] else 0.0