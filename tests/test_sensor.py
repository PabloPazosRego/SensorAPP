import unittest
from unittest.mock import patch
import random
from src.sensor import Sensor

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


if __name__ == "__main__":
    unittest.main()