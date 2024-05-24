import sqlite3  # Para SQLite
from nats.aio.client import Client as NATS
import random, argparse, time

# Creacion Base de Datos

class Database:
    def __init__(self, db_url) -> None:
        self.db_url = db_url
        #self.db_conn = sqlite3.connect(db_url)
        self.create_connection()
        
    def create_connection(self):
        try:
            self.db_conn = sqlite3.connect(self.db_url)
        except Exception as e:
            print(f'Imposible conectar con la base de datos: {e}')
    
# Creacion del Sensor
class Sensor:
    def __init__(self):
        return
    def read_sensor_data(self):
        ''' Leer datos del sensor, 
        inicialmente generamos datos aleatorios en el formato del sensor real'''
        return [random.randint(0, 100) for _ in range(64)]
    

class DataPublisher:
    '''
        Clase para gestionar la publicacion de los datos del sensor al NATS
    '''
    def __init__(self) -> None:
        self.nats_client = NATS()
        self.connect_to_nats()

    def connect_to_nats(self):
        self.nats_client.connect('nats://localhost:4222')
    
    def publish_data(self, data):
        self.nats_client.publish('sensor.data', str(data).encode())


'''
    Inicializacion del programa
    Se añaden los argumentos solicitados para introducir cada vez que se ejecute la APP se puedan modificar en la llamada.
'''
def main():
    parser = argparse.ArgumentParser(description="Sensor Application")
    parser.add_argument("--frequency", type=int, default=5, help="Frecuencia de lectura del sensor en segundos.")
    parser.add_argument("--db_uri", default="sqlite:///sensor_data.db", help="URL de conexion a la base de datos.")

    args = parser.parse_args()

    sensor = Sensor()
    data_publisher = DataPublisher()
    database = Database(args.db_uri)

    while True:
        data = sensor.read_sensor_data()
        data_publisher.publish_data(data)
        time.sleep(args.frequency) #Paralizar la solicitud de datos el tiempo marcado como frecuencia

if __name__ == "__main__":
    main()