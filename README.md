# Sensor Data Application

## Descripción

Esta aplicación escrita en Python está diseñada para leer datos de un sensor infrarrojo (real o mockup), publicarlos en un servidor NATS cada cierto intervalo de tiempo, atender peticiones para iniciar y detener la captura de datos y almacenar la información en una base de datos SQL.

## Características

- Lectura de datos del sensor cada `n` segundos.
- Posibilidad de iniciar o detener la captura de datos del sensor y la publicación de datos asociada.
- Almacenamiento de los datos capturados en una base de datos SQL.
- Diferenciación entre un sensor real y un mockup.
- Publicación de los datos utilizando el protocolo NATS.

## Instalación

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/tu_usuario/sensor-data-application.git
    cd sensor-data-application
    ```

2. Crear un entorno virtual e instalar las dependencias:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows, usar `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Uso

### Ejecución de la Aplicación

La aplicación puede ser ejecutada desde la línea de comandos con varios argumentos:

```bash
python main.py --frequency <SEGUNDOS> --db_uri <URL_BASE_DATOS> --sensor_type <REAL/MOCKUP> --serial_port <PUERTO_SERIE_SENSOR>

