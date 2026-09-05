import socket
import threading
from storage import enusuarios, logeao, ensesionado

# Diccionario global para guardar los sockets de los clientes logeados
# Formato: { "token123": objeto_socket }
candado_clientes_activos = threading.Lock()
clientes_activos = {}

def manejar_cliente(conn, addr):
    print(f"[TCP] Cliente conectado desde {addr}")
    with conn:
        while True:
            try:
                datos = conn.recv(1024).decode('utf-8')
                if not datos:
                    break # El cliente se desconectó físicamente
                
                partes = datos.strip().split(" ")
                comando = partes[0]

                if comando == "LOGIN" and len(partes) >= 3:
                    user = partes[1]
                    password = partes[2]

                    if enusuarios(user, password):
                        token = logeao(user)
                        #tomamos el candado
                        with candado_clientes_activos:
                            clientes_activos[token] = conn # Guardamos el socket
                        # Enviamos OK, el token, y el PUERTO UDP DEL SERVIDOR (9001)
                        conn.sendall(f"OK {token} 9001\n".encode('utf-8'))
                        print(f"[TCP] Login exitoso: {user}")
                    else:
                        conn.sendall("ERROR INVALID CREDENTIALS\n".encode('utf-8'))

                elif comando == "MSG" and len(partes) >= 3:
                    token = partes[1]
                    mensaje = " ".join(partes[2:])
                    
                    usuario = ensesionado(token,mensaje)
                    if usuario:
                        conn.sendall("ACK\n".encode('utf-8'))

                        #Tomamos el candado para ver a los clientes activos y hacer el broadcast
                        with candado_clientes_activos:
                            for token_destino, socket_destino in clientes_activos():
                                #nos aseguramos de no mandarnos el mensaje a nosotros mismos
                                if token_destino != token:
                                    try:
                                        socket_destino.sendall(f"INCOMING {usuario} {mensaje}\n".encode('utf-8'))
                                    except Exception:
                                        pass
                    else:
                        conn.sendall("ERROR INVALID TOKEN OR EXPIRED\n".encode('utf-8'))
            except Exception as e:
                print(f"[TCP] Error con {addr}: {e}")
                break

# -------------------Funcion----------------------
#   expulsarClienteTCP:
#       Se encargara de expulsar del socker a las sesiones cerradas 
#  ------------------Parametros-------------------
#   token_objetivo:
#       token objetivo para expulsar del socketr
#  ------------------Return-----------------------
#  None
#  -----------------------------------------------
def expulsarClienteTCP(token_objetivo):
    #tomamos el candado
    with candado_clientes_activos:
        if token_objetivo in clientes_activos[token_objetivo]:
            socket_objetivo = clientes_activos[token_objetivo]
            #eliminamos dentro de un bloque try
            try:
                socket_objetivo.sendall("ERROR SESSION EXPIRED\n".encode('utf-8'))
                socket_objetivo.close()
            except Exception:
                pass
            
            #eliminamos el token asesinado de nuestra lista
            del clientes_activos[token_objetivo]

def innit_tcp(host="0.0.0.0", port=9000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"[TCP] Servidor escuchando en {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            # Creamos un hilo independiente para cada cliente que llega
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo_cliente.start()