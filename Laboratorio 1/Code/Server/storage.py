#-------------------------Librerias-----------------------
import csv
import threading
import time
import os

# Creacion de candados para proteger el manejo de CSV
candado_sesion = threading.Lock()
candado_usuarios = threading.Lock()
candado_historial = threading.Lock()

# Definimos las direcciones de cada .csv.
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
RUTA_USUARIOS = os.path.join(DATA_DIR, "usuarios.csv")
RUTA_SESIONES = os.path.join(DATA_DIR, "sesiones.csv")
Ruta_HISTORIAL = os.path.join(DATA_DIR, "historial.csv")

#---------------------- Variables ---------------------------
