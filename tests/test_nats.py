
import unittest
from unittest.mock import patch, AsyncMock, Mock
import asyncio, random

from src.nats_client import DataPublisher

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


if __name__ == "__main__":
    unittest.main()