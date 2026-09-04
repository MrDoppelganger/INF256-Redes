#-------------------------------Liberia---------------------------
import time
import csv
from storage import candado_sesion, RUTA_SESIONES

#-------------------------------Funciones--------------------------
# -------------------Funcion----------------------
#   innit_watchdog:
#       Ciclo infinito que va revisando el estado de las sesiones
#       cada 5 segundos y duerme entre cada revision.
#  ------------------Parametros-------------------
#  NONE
#  ------------------Return-----------------------
#  Void: NONE
def innit_watchdog():
    print("[Watchdog] inicializandose monitoreo de inactividad..")
    #Nos metemos en un bucle infinito para realizar las revisiones constantemente
    while True:
        #dejamos durmiendo al watchdog en el intermedio de cada revision
        time.sleep(5)
        tiempo_actual = time.time()
        sesiones_actualizadas = []

        #Agarramos el candado de acceso a la bd de sesiones
        with candado_sesion:
            #leemos el estado de las sesiones
            with open(RUTA_SESIONES, modo = 'r', encoding = 'utf-8') as f:
                lector = csv.reader(f)
                #revisamos todas las sesesiones de la bd
                for fila in lector:
                    #Comprobamos si es que cumple el formato y es una sesion activa
                    if len(fila) == 5 and fila[4] == "ACTIVA":
                        tiempo_creacion = float(fila[2])
                        tiempo_ultimo_hb = float(fila[3])

                        #Condiciones para matar la sesion
                        #No ha habido Heartbeat despues de 30 segundos desde la creación
                        expiracion_tiempo_gracia = (tiempo_creacion == tiempo_ultimo_hb) and (tiempo_actual - tiempo_creacion > 30)
                        # Han pasado mas de 60 segundos desde el ultimo HEARTBEAT
                        desconexion = (tiempo_creacion != tiempo_ultimo_hb) and (tiempo_actual - tiempo_ultimo_hb > 60)
                        # Sesion expirada por tiempo limite de 10 minutos
                        sesion_expirada = (tiempo_actual - tiempo_creacion > 600)

                        #si se cumple cualquiera de las condiciones, expiramos la sesion
                        if expiracion_tiempo_gracia or desconexion or sesion_expirada:
                            fila[4] = "EXPIRADO"
                            print(f"[Watchdog] Sesion {fila[0]} Aniquilada")
                            #Nota: Aqui hay que avisarle al server_tcp que cierre el socket fisico

                    sesiones_actualizadas.append(fila)
            #Actualizamos las sesiones
            with open(RUTA_SESIONES, mode = 'w', encoding = 'utf-8') as f:
                actualizador = csv.writer(f)
                actualizador.writerow(sesiones_actualizadas)
