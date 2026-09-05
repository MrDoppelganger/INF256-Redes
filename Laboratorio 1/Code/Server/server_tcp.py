import socket
import threading
from storage import verificar_credenciales, crear_sesion, validar_token_y_obtener_usuario

# Diccionario global para guardar los sockets de los clientes logeados
# Formato: { "token123": objeto_socket }
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

                    if verificar_credenciales(user, password):
                        token = crear_sesion(user)
                        clientes_activos[token] = conn # Guardamos el socket
                        # Enviamos OK, el token, y el PUERTO UDP DEL SERVIDOR (9001)
                        conn.sendall(f"OK {token} 9001\n".encode('utf-8'))
                        print(f"[TCP] Login exitoso: {user}")
                    else:
                        conn.sendall("ERROR INVALID CREDENTIALS\n".encode('utf-8'))

                elif comando == "MSG" and len(partes) >= 3:
                    token = partes[1]
                    mensaje = " ".join(partes[2:])
                    
                    usuario = validar_token_y_obtener_usuario(token)
                    if usuario:
                        # Aquí deberías guardar el mensaje en historial.csv usando storage.py
                        # Y luego hacer el BROADCAST a los demás
                        conn.sendall("ACK\n".encode('utf-8'))
                    else:
                        conn.sendall("ERROR INVALID TOKEN OR EXPIRED\n".encode('utf-8'))
            except Exception as e:
                print(f"[TCP] Error con {addr}: {e}")
                break

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