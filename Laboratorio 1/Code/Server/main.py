import threading
from server_http import innit_http
from server_udp import innit_udp
from watchdog import innit_watchdog
from server_tcp import innit_tcp

if __name__ == "__main__":
    print("[Server] Arrancando sistema central...")

    #Creamos los hilos de cada funcionalidad
    hilo_http = threading.Thread(target = innit_http, daemon= True)
    hilo_tcp = threading.Thread(target = innit_tcp, daemon= True)
    hilo_udp = threading.Thread(target = innit_udp, daemon= True)
    hilo_watchdog = threading.Thread(target = innit_watchdog, daemon= True)

    #Corremos nuestros hilos
    hilo_http.start()
    hilo_tcp.start()
    hilo_udp.start()
    hilo_watchdog.start()

    #Fijamos el main haciendo que escuche al hilo de tcp para que el codigo no acabe.
    hilo_tcp.join()