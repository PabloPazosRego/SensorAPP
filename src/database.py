import sqlite3  # Para SQLite
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    ''' 
        Gestion de la base de datos: creación y subida de datos
    '''

    def __init__(self, db_url) -> None:
        self.db_url = db_url
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.db_conn = sqlite3.connect(self.db_url)
            logging.info(f'DB:: Successful connection.')
        except Exception as e:
            logging.error(f'DB:: Unable to connect to the database: {e}')
            

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            value TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                          )''')
        self.db_conn.commit()

    def store_data(self, data):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO sensor_data (value) VALUES (?)", (str(data),))
            self.db_conn.commit()
            logging.info(f'DB:: Data stored correctly.')
        except sqlite3.Error as e:
            logging.error(f"DB:: Error storing data in database: {e}")