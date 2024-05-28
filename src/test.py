import unittest
from unittest.mock import patch, AsyncMock, Mock
import asyncio, random
from SensorAPP import Sensor, DataPublisher, Database

class TestSensor(unittest.TestCase):
    @patch('serial.Serial')
    def test_read_sensor_data_mockup(self, mock_serial):
        sensor = Sensor(sensor_type='mockup')
        data = sensor.read_sensor_data()
        self.assertEqual(len(data), 64)
        self.assertTrue(all(0 <= x <= 65535 for x in data))

    @patch('serial.Serial')
    def test_read_sensor_data_real(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.read.return_value = bytes([random.randint(0, 255) for _ in range(128)])
        sensor = Sensor(sensor_type='real')
        data = sensor.read_sensor_data()
        self.assertEqual(len(data), 64)
        self.assertTrue(all(0 <= x <= 65535 for x in data))

class TestDataPublisher(unittest.TestCase):
    @patch("SensorAPP.NATS")
    def setUp(self, MockNATS):
        self.nats_client = MockNATS.return_value
        self.data_publisher = DataPublisher()
        self.data_publisher.nats_client = self.nats_client

        # Mocking the async methods with AsyncMock
        self.data_publisher.nats_client.connect = AsyncMock()
        self.data_publisher.nats_client.publish = AsyncMock()

    def test_publish_data(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._test_publish_data())
        loop.close()

    async def _test_publish_data(self):
        data = [random.randint(0, 100) for _ in range(64)]
        await self.data_publisher.connect_to_nats()
        await self.data_publisher.publish_data(data)
        self.nats_client.publish.assert_called_with("sensor.data", str(data).encode())


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
