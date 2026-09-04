import socket
import datetime
from datetime import datetime,timedelta

def enusuarios(usuario,contra):
    with open("usuarios.csv", "r") as archivo: 
        for linea in archivo:
            partes = linea.strip().split(',')
            if usuario ==partes[0]:
                if contra==partes[1]:
                    return True
            else:
                pass
        print("ERROR INVALID CREDENTIALS. \n")
        return False
                                

def server():
    host = "127.0.0.1"
    port = 8080
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor escuchando en {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Conectado a {addr}")
            while True:
                datos= conn.recv(1024).decode('utf-8')
                partes = datos.strip().split(" ")
                comando = partes[0]

                if not datos:
                    break

                if comando == "LOGIN":
                    user=partes[1]
                    password=partes[2]

                    

                    if enusuarios(user,password):
                        #aqui creare las partes, strftime("%Y-%m-%d %H:%M:%S") esto es pa dejarlo como string leible

                        formato="%Y-%m-%d %H:%M:%S"
                        ahora = datetime.now()

                        timestamp_creacion=ahora.strftime(formato)
                        timestamp_ultimo_heartbeat=timestamp_creacion

                        vence=(ahora + timedelta(minutes=10)).strftime(formato)
                        texto = user + str(addr)
                        token= str(abs(hash(texto)))
                        estado="ACTIVO"
                        puerto_cliente=str(addr[1])

                        #print("llego con usuario " + user , password)
                        with open("sesiones.csv", "a") as archivo: 
                            archivo.write(f"{token},{user},{timestamp_creacion},{timestamp_ultimo_heartbeat},{estado}\n")
                        print(f"Sesión creada para {user} con token {token}")
                        conn.sendall(f"OK {token} {puerto_cliente}\n".encode('utf-8'))

                    else:
                        conn.sendall(f"ERROR INVALID CREDENTIALS\n".encode('utf-8'))
                        continue



                    
                elif comando == "MSG":
                    destino=partes[1]
                    
                    

                else:
                    print("no ta")


if __name__ == "__main__":
    server()