from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import csv
import json
from storage import comprobar_existencia_username, añadir_usuario, leer_historial

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

# -------------------Funcion----------------------
#   innit_http:
#        Se encarga de levantar las funcionalidades del HTTP
#  ------------------Parametros-------------------
#   host = "0.0.0.0": 
#       Fijamos el host con el INADDR_ANY que le dice al
#       socket que debera de escuchar en todas las interfaces
#       de red disponible
#   port = 8080:
#       Establecemos que el puerto de comunicacion sera el 
#       8080
#  ------------------Return-----------------------
#  Void: NONE
#  -----------------------------------------------
def innit_http(host = "0.0.0.0", port = 8080):
    servidor = ThreadingHTTPServer((host, port), ServidorRedes)
    print(f"[HTTP] Servidor ejecutandose en http://{host}:{port}")
    servidor.serve_forever()