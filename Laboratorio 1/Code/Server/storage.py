#---------------------------------Librerias---------------------------------
import csv
import threading
import time
import os

#----------------------------Variables generales---------------------------
# Definimos las rutas de nuestra "Base de Datos" persistente
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
RUTA_USUARIOS = os.path.join(DATA_DIR, "usuarios.csv")
RUTA_SESIONES = os.path.join(DATA_DIR, "sesiones.csv")
Ruta_HISTORIAL = os.path.join(DATA_DIR, "historial.csv")

# Creacion de candados para proteger el multi acceso a la "BD"
candado_sesion = threading.Lock()
candado_usuarios = threading.Lock()
candado_historial = threading.Lock()

#--------------------------------Funciones--------------------------------
# -------------------Funcion----------------------
#   actulizarHeartbeat:
#       Actualiza el valor del ultimo tiempo en el que se recibio un 
#       heartbeat y lo reemplaza por el valor del tiempo actual.
#  ------------------Parametros-------------------
#  token_objetivo: 
#       Es el token de la sesion que queremos actualizar
#  ------------------Return-----------------------
#  Void: NONE
#  -----------------------------------------------
def actualizarHeartbeat(token_objetivo):
    #obtenemos los valores iniciales
    tiempo_actual = str(time.time())
    sesiones_actualizadas = []

    #tomamos el candado para leer el csv de sesiones
    with candado_sesion:
        #Leemos y recolectamos la info
        with open(RUTA_SESIONES, mode = 'r', encoding = 'utf-8') as f:
            lector = csv.reader(f)
            for fila in lector:
                #Buscamos el token de la sesion que queremos actualizar
                if len(fila) == 5 and fila[0] == token_objetivo and fila[4] == "ACTIVO":
                    #Si pasamos la evaluación de cortocircuito y encontramos la sesion, actualizamos
                    fila[3] = tiempo_actual
                sesiones_actualizadas.append(fila)
        #Actualizamos las sesiones
        with open(RUTA_SESIONES, mode = 'w', encoding = 'utf-8') as f:
            actualizador = csv.writer(f)
            actualizador.writerow(sesiones_actualizadas)
