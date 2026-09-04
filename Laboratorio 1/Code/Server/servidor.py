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
                                
def logeao(conn, addr, user):
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

def ensesionao(token,mensaje,conn):
    with open("sesiones.csv", "r") as archivo: 
            for linea in archivo:
                partes = linea.strip().split(',')
                if token == partes[0]:
                    username=partes[1]
                    ahora = datetime.now()
                    formato="%Y-%m-%d %H:%M:%S"
                    
                    #saque el de creacion
                    t_creao = datetime.strptime(partes[2], formato)

                    #saque el de ultimo
                    t_terminao = datetime.strptime(partes[3], formato)

                    desde_creao=(ahora-t_creao).total_seconds()
                    desde_terminao=(ahora-t_terminao).total_seconds()
                    if partes[4]=="ACTIVO":
                        if desde_creao<=600 and desde_terminao<=60:
                            time=ahora.strftime(formato)
                            return time,username, mensaje
                        else:
                            conn.sendall("ERROR SESSION EXPIRED\n".encode('utf-8'))
                            return False
                        
                else:
                    pass
            conn.sendall("ERROR INVALID TOKEN\n".encode('utf-8'))
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

                    #aqui va mi bloque gigante de codigo
                    if enusuarios(user,password):
                        logeao(conn, addr, user)
                        
                    else:
                        conn.sendall(f"ERROR INVALID CREDENTIALS\n".encode('utf-8'))
                        continue



                    
                elif comando == "MSG":
                    token=partes[1]
                    mensaje=" ".join(partes[2:])
                    resultado=ensesionao(token,mensaje,conn)
                    if resultado:
                        time, user, msg = resultado
                        with open("historial.csv", "a") as hist:
                            hist.write(f"{time},{user},{msg}\n")
                            conn.sendall(f"ACK\n".encode('utf-8'))


                else:
                    print("no ta")


if __name__ == "__main__":
    server()