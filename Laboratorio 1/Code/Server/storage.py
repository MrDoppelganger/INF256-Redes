#---------------------------------Librerias---------------------------------
import csv
import threading
import time
import os
from datetime import datetime


#----------------------------Variables generales---------------------------
# Definimos las rutas de nuestra "Base de Datos" persistente
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
RUTA_USUARIOS = os.path.join(DATA_DIR, "usuarios.csv")
RUTA_SESIONES = os.path.join(DATA_DIR, "sesiones.csv")
RUTA_HISTORIAL = os.path.join(DATA_DIR, "historial.csv")

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

# -------------------Funcion----------------------
#   comprobar_existencia_username:
#       Revisa si el usuario ya esta registrado dentro de nuestra bd 
#  ------------------Parametros-------------------
#   a: 
#       Es el username del usuario que queremos buscar
#  ------------------Return-----------------------
#   bool: retornamos 1 si encontramos y cero en caso contrario
#  -----------------------------------------------
def comprobar_existencia_username(a):
    #Tomamos el candado del csv de usuarios
    with candado_usuarios:
        with open(RUTA_USUARIOS, newline = '', encoding = 'utf-8') as archivo:
            lector = csv.reader(archivo)
            for username in lector:
                if username[0] == a:
                    return 1
            return 0

# -------------------Funcion----------------------
#   añadir_usuario:
#       Añadimos un nuevo usuario a nuestra bd 
#  ------------------Parametros-------------------
#   user: 
#       Es el username del usuario que queremos agregar
#   password:
#       Es la contraseña del usuario que queremos agregar
#  ------------------Return-----------------------
#  void: None.
#  -----------------------------------------------
def añadir_usuario(user,pasword):
    #Tomamos el candado para el usuario.csv
    with candado_usuarios:
        with open(RUTA_USUARIOS, mode = 'a', newline= '',encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([user,pasword,datetime.now()])
            
# -------------------Funcion----------------------
#   leer_historial:
#       entrega el historial actual 
#  ------------------Parametros-------------------
# NONE
#  ------------------Return-----------------------
#  historial_mensaje: es una lista con todas las filas de la bd de historial.
#  -----------------------------------------------
def leer_historial():
    #Tomamos el candado del historial
    with candado_historial:
        historial_mensajes = []

        with open(RUTA_HISTORIAL, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)

            for fila in lector:
                historial_mensajes.append(fila)

        return historial_mensajes