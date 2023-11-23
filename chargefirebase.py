# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 23:24:42 2023

@author: ivan
"""

from firebase_admin import credentials
from firebase_admin import firestore

# Ruta al archivo de credenciales de Firebase (descargado previamente)
cred = credentials.Certificate("literatura-71c26-firebase-adminsdk-qjq76-9ef22ce2d2.json")

# Inicializar la aplicación de Firebase
# firebase_admin.initialize_app(cred)

# Obtener una referencia a la base de datos Firestore
db = firestore.client()

# Cargar datos en la colección
import json

# Leer el archivo JSON
with open("emigracion.txt.json", "r") as archivo:
    data = json.load(archivo)

# Acceder a los datos


# Especificar la ruta a la colección donde deseas cargar los datos
coleccion_ref = db.collection("tema")

# Añadir los datos a la colección
for d in data:
    coleccion_ref.add(d)

print("Datos cargados exitosamente en la colección.")