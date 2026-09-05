package main

import (
	"fmt"
	"net"
	"time"
)

func IniciarHeartbeatUDP(token string) {
	host := "127.0.0.1"
	port := "9001" // El puerto UDP de tu servidor

	// Conexión UDP
	conn, err := net.Dial("udp", host+":"+port)
	if err != nil {
		fmt.Println("[UDP] Error conectando:", err)
		return
	}
	defer conn.Close()

	// Creamos un temporizador que se ejecute cada 20 segundos
	ticker := time.NewTicker(20 * time.Second)
	defer ticker.Stop()

	mensaje := fmt.Sprintf("HEARTBEAT %s", token)

	fmt.Println("[UDP] Iniciando envío de latidos en segundo plano...")

	// Bucle infinito que espera los "ticks" del temporizador
	for {
		<-ticker.C // Espera a que pasen los 20 segundos
		_, err := fmt.Fprint(conn, mensaje)
		if err != nil {
			fmt.Println("[UDP] Error enviando heartbeat:", err)
			break // Rompe el bucle si se pierde la conexión física
		}
		// Opcional: imprimir en consola para confirmar que funciona en tus pruebas
		// fmt.Println("[UDP] Heartbeat enviado")
	}
}
