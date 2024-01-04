#Gestion de la conección con la base de datos
from pymongo import MongoClient

url='mongodb://localhost:27017/'
base_datos='local'
coleccion='users'

def conectar_base_datos():
    try:
        db_client = MongoClient(url)
        db = db_client[base_datos]
        collection = db[coleccion]

        return collection
    except Exception as e:
        print(f"Error al conectar a la base de datos : {e}")
        return None
    
try:
    conexion = conectar_base_datos()
    print("Conexión a la base de datos exitosa")
except RuntimeError as e:
    print(f"Error: error al momento de conectar la base de datos {e}")