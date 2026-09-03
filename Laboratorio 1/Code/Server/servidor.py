import socket

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
                    print("llego con usuario " + user , password)
                    
                    #token =
                    #with open("sesiones.csv", "w") as archivo: 
                     #   archivo.write(token +"," creacion+ "," + timestamp +"," + ultimo_heartbeat +"," estado)



                    
                elif comando == "MSG":
                    destino=partes[1]
                    
                    

                else:
                    print("no ta")


if __name__ == "__main__":
    server()