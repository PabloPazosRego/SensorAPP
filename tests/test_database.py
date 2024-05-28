import unittest
import random
from src.database import Database

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        self.database = Database(":memory:")  # Usar una base de datos en memoria para pruebas

    def test_store_data(self):
        data = [random.randint(0, 65535) for _ in range(64)]  # Valores de 16 bits sin signo
        try:
            self.database.store_data(data)
            cursor = self.database.db_conn.cursor()
            cursor.execute("SELECT value FROM sensor_data")
            stored_data = cursor.fetchone()[0]
            self.assertEqual(stored_data, str(data))
        except Exception as e:
            self.fail(f"store_data raised Exception unexpectedly: {e}")

if __name__ == "__main__":
    unittest.main()