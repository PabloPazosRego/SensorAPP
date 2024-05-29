import serial
import logging, random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Sensor:
    '''
        Objeto del sensor, pudiendo generar diferentes sensores. 
        Se gestiona si la cogida de datos es artificial o de un sensor real.
    '''
    def __init__(self, sensor_type, serial_port =None, baud_rate = None, max_mockup = 100, min_mockup = 0):
        """Constructor del sensor.

        Args:
            sensor_type (str): Tipo de sensor ("mockup" o "real").
            serial_port (str, optional): Puerto serial del sensor. Defaults to None.
            baud_rate (int, optional): Velocidad de baudios. Defaults to None.
        """

        self.sensor_type = sensor_type
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.min_mockup = min_mockup
        self.max_mockup = max_mockup
        if sensor_type == 'real':
            self.connect_sensor()
        return
    
    def connect_sensor(self):
        '''
            Conexion del sensor real por puerto serie. 
        '''
        try:
            self.serial_conn = serial.Serial(self.serial_port, self.baud_rate)
        except Exception as e:
             logging.error(f"SENSOR:: Error opening serial port: {e}")

    
    def read_sensor_data(self):
        ''' 
         Returns
        
            A list of 64 unsigned 16-bit integers.
        '''
        if self.sensor_type == 'mockup':
            return [random.randint(self.min_mockup, self.max_mockup) for _ in range(64)]
        else:
            if self.serial_conn.is_open:
                try:
                    # Leer datos del puerto serie
                    data = self.serial_conn.read(128)  # Leer 128 bytes (64 valores de 16 bits)
                    return [int.from_bytes(data[i:i+2], byteorder='little') for i in range(0, len(data), 2)]
                except Exception as e:
                    print(f"Error al leer datos del puerto serie: {e}")
                    return None
            else:
                print("El puerto serie no está abierto")
                return None