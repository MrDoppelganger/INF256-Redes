import socket
import threading
from storage import enusuarios, logeao, ensesionado

# Diccionario global y su candado para proteger la concurrencia
candado_clientes_activos = threading.Lock()
clientes_activos = {}

def manejar_cliente(conn, addr):
    print(f"[TCP] Cliente conectado desde {addr}")
    token_actual = None # para limpiar si se desconecta de forma física
    
    with conn:
        while True:
            try:
                datos = conn.recv(1024).decode('utf-8')
                if not datos:
                    break #el cliente se desconcto 
                
                partes = datos.strip().split(" ")
                if not partes:
                    continue
                comando = partes[0]

                if comando == "LOGIN" and len(partes) >= 3:
                    user = partes[1]
                    password = partes[2]

                    if enusuarios(user, password):
                        token = logeao(user)
                        token_actual = token
                        with candado_clientes_activos:
                            clientes_activos[token] = conn
                        # formato  OK <token> <puertoUDP>
                        conn.sendall(f"OK {token} 9001\n".encode('utf-8'))
                        print(f"[TCP] Login exitoso: {user}")
                    else:
                        conn.sendall(b"ERROR INVALID CREDENTIALS\n")

                elif comando == "MSG" and len(partes) >= 3:
                    token = partes[1]
                    mensaje = " ".join(partes[2:])
                    
                    usuario = ensesionado(token, mensaje)
                    if usuario:
                        conn.sendall(b"ACK\n")

                        #broadcast para que el otro cliente reciba el INCOMING
                        with candado_clientes_activos:
                            for token_destino, socket_destino in clientes_activos.items():
                                if token_destino != token:
                                    try:
                                        socket_destino.sendall(f"INCOMING {usuario}: {mensaje}\n".encode('utf-8'))
                                    except Exception:
                                        pass
                    else:
                        conn.sendall(b"ERROR INVALID TOKEN OR EXPIRED\n")
            except Exception as e:
                print(f"[TCP] Error con {addr}: {e}")
                break
                
        # Limpieza automática si el cliente se desconecta voluntariamente
        if token_actual:
            with candado_clientes_activos:
                if token_actual in clientes_activos:
                    del clientes_activos[token_actual]

def expulsarClienteTCP(token_objetivo):
    with candado_clientes_activos:
        if token_objetivo in clientes_activos:
            socket_objetivo = clientes_activos[token_objetivo]
            try:
                socket_objetivo.sendall(b"ERROR SESSION EXPIRED\n")
                socket_objetivo.close()
            except Exception:
                pass
            del clientes_activos[token_objetivo]
            print(f"[TCP] Cliente {token_objetivo} expulsado por el Watchdog.")

def innit_tcp(host="0.0.0.0", port=9000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"[TCP] Servidor escuchando en {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo_cliente.start()