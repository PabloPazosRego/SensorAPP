import sqlite3  # Para SQLite
from nats.aio.client import Client as NATS
import random, argparse, time
import asyncio, serial

# Creacion Base de Datos

class Database:
    def __init__(self, db_url) -> None:
        self.db_url = db_url
        #self.db_conn = sqlite3.connect(db_url)
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.db_conn = sqlite3.connect(self.db_url)
            print('Realizada conexion con exito')
        except Exception as e:
            print(f'Imposible conectar con la base de datos: {e}')
            

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
            print(str(data).encode())
            cursor.execute("INSERT INTO sensor_data (value) VALUES (?)", (str(data),))
            self.db_conn.commit()
        except sqlite3.Error as e:
            print(f'Error subiendo datos al DB {e}')
    
# Creacion del Sensor
class Sensor:
    def __init__(self, sensor_type, serial_port =None, baud_rate = None):
        self.sensor_type = sensor_type
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        if sensor_type == 'real':
            self.connect_sensor()
        return
    
    def connect_sensor(self):
        try:
            self.serial_conn = serial.Serial(self.serial_port, self.baud_rate)
        except Exception as e:
            print(f'Error en la conexion al sensor: {e}')
    
    def read_sensor_data(self):
        ''' Leer datos del sensor '''
        if self.sensor_type == 'mockup':
            return [random.randint(0, 100) for _ in range(64)]
        else:
            try:
                data = self.serial_conn.readline().decode().strip()
                return data
            except Exception as e:
                print(f'Error leyendo del sensor: {e}')

class DataPublisher:
    '''
        Clase para gestionar la publicacion de los datos del sensor al NATS
    '''
    def __init__(self) -> None:
        self.nats_client = NATS()
        #self.connect_to_nats()

    async def connect_to_nats(self):
        try:
            await self.nats_client.connect(servers=["nats://localhost:4222"], connect_timeout=10)

            #await self.nats_client.connect('nats://localhost:4222')
        except Exception as e:
            print(f'Imposible conectarse al servidor NATS {e}')
    
    async def publish_data(self, data):
        try:
            await self.nats_client.publish('sensor.data', str(data).encode())
        except Exception as e:
            print(f'Imposible publidar datos en el servidor NATS {e}')


'''
    Inicializacion del programa
    Se añaden los argumentos solicitados para introducir cada vez que se ejecute la APP se puedan modificar en la llamada.
'''
async def main():
    parser = argparse.ArgumentParser(description="Sensor Application")
    
    parser.add_argument("--sensor_type", choices=["mockup", "real"], default="mockup", help="Tipo de sensor: real o mockup")
    parser.add_argument("--serial_port", default="/dev/ttyUSB0", help="Puerto Serie del sensor")
    parser.add_argument("--baud_rate", type=int, default=9600, help="Baud rate para comunicación del puerto Serie.")
    parser.add_argument("--frequency", type=int, default=5, help="Frecuencia de lectura del sensor en segundos.")
    parser.add_argument("--db_uri", default="../sensor_data.db", help="URL de conexion a la base de datos.")

    args = parser.parse_args()

    sensor = Sensor(args.sensor_type, args.serial_port, args.baud_rate)
    data_publisher = DataPublisher()
    database = Database(args.db_uri)

    await data_publisher.connect_to_nats()

    while True:
        data = sensor.read_sensor_data()
        if data:
            await data_publisher.publish_data(data)
            database.store_data(data)
        #time.sleep(args.frequency) #Paralizar la solicitud de datos el tiempo marcado como frecuencia
        await asyncio.sleep(args.frequency)

if __name__ == "__main__":
    asyncio.run(main())