import threading
from server_http import innit_http
from server_udp import innit_udp
from watchdog import innit_watchdog

if __name__ == "__main__":
    print("[Server] Arrancando sistema central...")

    #Creamos los hilos de cada funcionalidad
    hilo_http = threading.Thread(target = innit_http, deamon = True)
    hilo_udp = threading.Thread(target = innit_udp, deamon = True)
    hilo_watchdog = threading.Thread(target = innit_watchdog, deamon = True)

    #Corremos nuestros hilos
    hilo_http.start()
    hilo_udp()
    hilo_watchdog()

    #Fijamos el main haciendo que escuche al hilo de HTTP para que el codigo no acabe.
    hilo_http.join()