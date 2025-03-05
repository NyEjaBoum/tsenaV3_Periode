# connexion.py
import pyodbc

class Connexion:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        try:
            conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.db_file
            self.conn = pyodbc.connect(conn_str)
            print("Connexion réussie à la base de données Access.")
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    def execute_query(self, query):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        return []

    def execute_update(self, query):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            print("Opération réussie.")
            
    def close(self):
        if self.conn:
            self.conn.close()
