import unittest
from unittest.mock import patch, AsyncMock, Mock
import asyncio, random
from SensorAPP import Sensor, DataPublisher, Database

class TestSensor(unittest.TestCase):
    def test_read_sensor_data_mockup(self):
        sensor = Sensor(sensor_type="mockup")
        data = sensor.read_sensor_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)

    def test_read_sensor_data_real(self):
        mock_serial = Mock()
        mock_serial.readline.return_value = "123,456\n"
        sensor = Sensor(sensor_type="real", serial_port="COM1", baud_rate=9600)
        sensor.serial_connection = mock_serial
        data = sensor.read_sensor_data()
        self.assertEqual(data, "123,456")

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
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_publish_data())

    async def _test_publish_data(self):
        data = [random.randint(0, 100) for _ in range(64)]
        await self.data_publisher.connect_to_nats()
        await self.data_publisher.publish_data(data)
        self.nats_client.publish.assert_called_with("sensor.data", str(data).encode())


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(db_uri="sqlite:///:memory:")
    
    def test_store_data(self):
        self.db.store_data("test_data")
        cursor = self.db.db_connection.cursor()
        cursor.execute("SELECT * FROM sensor_data")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "test_data")

if __name__ == "__main__":
    unittest.main()
