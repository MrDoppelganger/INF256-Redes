from http.server import HTTPServer, BaseHTTPRequestHandler
import csv
from datetime import datetime
import json

PORT = 8080
HOST = "127.0.0.1"


def comprobar_existencia_username(a):
    with open('usuarios.csv',newline= '',encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for username in lector:
            if username[0] == a:
                return 1
        return 0

def añadir_usuario(user,pasword):
    with open('usuarios.csv',mode='a', newline= '',encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([user,pasword,datetime.now()])
        
def leer_historial():
    historial_mensajes = []

    with open("historial.csv", "r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)

        for fila in lector:
            historial_mensajes.append(fila)

    return historial_mensajes

class ServidorRedes(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/history":
            historial_mensajes = leer_historial()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            response = json.dumps(historial_mensajes[-10:]).encode("utf-8")
            self.send_header("Content-Length", len(response))
            self.end_headers()
            self.wfile.write(response)


    def do_POST(self):
        if self.path == '/register':
            tamaño_bytes_mensaje = self.headers["Content-Length"]
            tamaño_bytes_mensaje = int(tamaño_bytes_mensaje)
            datos_registro = self.rfile.read(tamaño_bytes_mensaje)
            diccionario = json.loads(datos_registro)
            if "Username" in diccionario and "Password" in diccionario:
                usuario = diccionario["Username"]
                contraseña = diccionario["Password"]

                if usuario.strip() == "" or contraseña.strip() == "":
                    self.send_response(400, "Bad Request")
                    self.end_headers()
                    return

                retorno = comprobar_existencia_username(usuario)
                if retorno == 1:
                    self.send_response(409, "Conflict")
                    self.end_headers()
                else:
                    añadir_usuario(usuario,contraseña)
                    self.send_response(201, "Created")
                    self.end_headers()

            else:
                self.send_response(400, "Bad request")
                self.end_headers()

        

servidor = HTTPServer((HOST,PORT), ServidorRedes)
print(f"Servidor ejecutandose en http://{HOST}:{PORT}")

servidor.serve_forever()