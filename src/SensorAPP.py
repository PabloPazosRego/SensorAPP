
import random, argparse, time
import asyncio, logging
from sensor import Sensor
from database import Database
from nats_client import DataPublisher


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

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
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
        await asyncio.sleep(args.frequency) #Paralizar la solicitud de datos el tiempo marcado como frecuencia


if __name__ == "__main__":
    asyncio.run(main())