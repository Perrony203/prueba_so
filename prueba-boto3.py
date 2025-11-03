import boto3
import time
from boto3.s3.transfer import S3Transfer
import glob
from pathlib import Path

s3 = boto3.client('s3')
transfer = S3Transfer(s3)

# Carga del archivo al bucket
s3.upload_file('prueba-boto3.txt', 'user-spcjaga-smm-ueia-so', 'prueba-boto3.txt') 

# Verificación de carga del archivo 
for i in s3.list_objects_v2(Bucket = 'user-spcjaga-smm-ueia-so')['Contents']:
    print(i['Key'])
    
# Descarga en local 
s3.download_file('user-spcjaga-smm-ueia-so', 'prueba-boto3.txt', 'descargas/descarga-boto3.txt')

# Carga de multiples archivos
list(map(lambda f: transfer.upload_file(f, 'user-spcjaga-smm-ueia-so', f.split('/')[-1]), glob.glob('textos/punto-2/*.txt')))

# Descarga de múltiples archivos
archivos = [obj['Key'] for obj in s3.list_objects_v2(Bucket = 'user-spcjaga-smm-ueia-so')['Contents']
            if obj['Key'].startswith("2-") and obj['Key'].endswith('.txt')]

list(map(lambda f: s3.download_file('user-spcjaga-smm-ueia-so', f, str(Path('descargas/punto-2') / f)), archivos))