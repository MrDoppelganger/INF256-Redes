package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

// Hilo secundario para leer los mensajes que llegan del servidor (Broadcast)
func escucharServidor(conn net.Conn) {
	reader := bufio.NewReader(conn)
	for {
		respuesta, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("\n[TCP] Conexión perdida con el servidor.")
			os.Exit(0)
		}
		fmt.Printf("\n[MENSAJE ENTRANTE] %s>> ", respuesta)
	}
}

func IniciarChatTCP() {
	conn, err := net.Dial("tcp", "127.0.0.1:9000")
	if err != nil {
		fmt.Println("Error conectando al servidor TCP:", err)
		return
	}
	defer conn.Close()

	fmt.Println("--- CLIENTE TCP ---")
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Inicie sesion (LOGIN usuario password): ")
	texto, _ := reader.ReadString('\n')
	fmt.Fprint(conn, texto)

	// Leer respuesta del servidor (OK <token> <puerto>)
	respServer, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		fmt.Println("Error leyendo respuesta:", err)
		return
	}
	fmt.Print("Servidor: ", respServer)

	// Si el login es exitoso, extraemos el token y disparamos las goroutines
	if strings.HasPrefix(respServer, "OK") {
		partes := strings.Split(strings.TrimSpace(respServer), " ")
		if len(partes) >= 2 {
			token := partes[1]

			// 1. Lanzamos el envío de latidos UDP en segundo plano
			go IniciarHeartbeatUDP(token)

			// 2. Lanzamos el receptor de mensajes TCP en segundo plano
			go escucharServidor(conn)

			fmt.Printf("\n[Sesión Iniciada] Token: %s\n", token)
			fmt.Println("Escribe tu mensaje (ej: MSG <token> hola) o 'SALIR' para terminar.\n")

			// Bucle principal para enviar mensajes de chat
			for {
				fmt.Print(">> ")
				linea, _ := reader.ReadString('\n')
				comandoLimpio := strings.TrimSpace(linea)

				if comandoLimpio == "SALIR" {
					fmt.Println("Cerrando sesión...")
					break
				}

				if comandoLimpio != "" {
					fmt.Fprint(conn, linea)
				}
			}
		}
	} else {
		fmt.Println("Autenticación fallida.")
	}
}
