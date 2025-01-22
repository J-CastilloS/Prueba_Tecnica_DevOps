import boto3
import json
import psycopg2
import os

# Configuración
S3_BUCKET = os.environ['S3_BUCKET']
REDSHIFT_HOST = os.environ['REDSHIFT_HOST']
REDSHIFT_PORT = int(os.environ['REDSHIFT_PORT'])
REDSHIFT_DB = os.environ['REDSHIFT_DB']
REDSHIFT_USER = os.environ['REDSHIFT_USER']
REDSHIFT_PASSWORD = os.environ['REDSHIFT_PASSWORD']
REDSHIFT_TABLE = os.environ['REDSHIFT_TABLE']

def lambda_handler(event, context):
    # Conexión a S3
    s3_client = boto3.client('s3')

    # Conexión a Redshift
    conn = psycopg2.connect(
        dbname=REDSHIFT_DB,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD,
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT
    )
    cursor = conn.cursor()

    try:
        # Leer detalles del evento
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']

            # Descargar archivo de S3
            file_path = f'/tmp/{object_key.split("/")[-1]}'
            s3_client.download_file(bucket_name, object_key, file_path)

            # Procesar archivo (ejemplo: leer JSON)
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Preparar datos para Redshift
            rows = [
                (item['id'], item['text'], item['timestamp'])
                for item in data['records']
            ]

            # Insertar en Redshift
            cursor.executemany(
                f"INSERT INTO {REDSHIFT_TABLE} (id, text, timestamp) VALUES (%s, %s, %s)", rows
            )
            conn.commit()

        return {"statusCode": 200, "body": "Processing completed successfully"}

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return {"statusCode": 500, "body": "An error occurred"}

    finally:
        cursor.close()
        conn.close()