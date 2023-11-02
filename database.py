import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect("employee_db.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, full_name TEXT, phone TEXT, email TEXT, salary INTEGER)")
        self.con.commit()

    def insert_data(self, full_name, phone, email, salary):
        self.cur.execute("INSERT INTO employees (full_name, phone, email, salary) VALUES (?, ?, ?, ?)", (full_name, phone, email, salary))
        self.con.commit()
