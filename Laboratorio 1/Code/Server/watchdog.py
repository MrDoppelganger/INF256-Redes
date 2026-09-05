#-------------------------------Liberia---------------------------
import time
from storage import expiradorSesiones
from server_tcp import expulsarClienteTCP
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
        #Hacemos dormir 5 segundos a nuestro watchdog por cada iteracion
        time.sleep(5)

        #Revisamos y expiramos todas las sesiones que cumplan con las condiciones
        expirados = expiradorSesiones()

        #Mostramos todas las sesiones que han sido expiradas
        for token in expirados:
            print(f"[WATCHDOG] Sesión {token} REVOCADA.")
            expulsarClienteTCP(token)