#-----------------------------------Librerias-------------------------
import socket
from storage import actualizarHeartbeat

#-----------------------------------Funciones-------------------------
# -------------------Funcion----------------------
#   innit_udp:
#        se encarga de crear un socket UDP puro para escuchar
#       las comunicaciones de los heartbeat.
#  ------------------Parametros-------------------
#   host = "0.0.0.0": 
#       Fijamos el host con el INADDR_ANY que le dice al
#       socket que debera de escuchar en todas las interfaces
#       de red disponible
#   port = 9001:
#       Establecemos que el puerto de comunicacion sera el 
#       9001
#  ------------------Return-----------------------
#  Void: NONE
#  -----------------------------------------------
def innit_udp(host = "0.0.0.0", port = 9001):
    #Solicitamos al SO la creacion de un descriptor de socket (direccion IPv4, datagrams en udp)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        #Asociamos el socket a nuestro host y puerto
        sock.bind((host,port))
        print(f"[Conexion UDP] Escuchando Heartbeats en {host}:{port}")

        #Iniciamos un bucle infinito para estar atento siempre
        while True:
            #Recibimos hearbeat de hasta 1024 byte y la direccion del remitente
            datos, adrr = sock.recvfrom(1024)
            mensaje = datos.decode('utf-8').strip()

            #Validamos el formato
            partes = mensaje.split(" ")
            if len(partes) == 2 and partes[0] == "HEARTBEAT":
                #si es un mensaje valido, mandamos a actualizar el valor del token
                token = partes[1]
                actualizarHeartbeat(token)