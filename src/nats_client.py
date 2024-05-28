from nats.aio.client import Client as NATS
import random, argparse, time
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        except Exception as e:
            logging.error(f"NATS:: Error connecting to NATS server: {e}")
    
    async def publish_data(self, data):
        try:
            await self.nats_client.publish('sensor.data', str(data).encode())
        except Exception as e:
            logging.error(f"NATS:: Error publishing data to NATS server: {e}")