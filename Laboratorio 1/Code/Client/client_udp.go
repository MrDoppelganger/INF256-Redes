package main

import (
	"fmt"
	"net"
	"time"
)

func IniciarHeartbeatUDP(token string, port string) {
	host := "127.0.0.1"
	conn, err := net.Dial("udp", host+":"+port)
	if err != nil {
		fmt.Println("[UDP] Error conectando:", err)
		return
	}
	defer conn.Close()

	// Ajustado a 3 segundos exactos según los requisitos del laboratorio
	ticker := time.NewTicker(3 * time.Second)
	defer ticker.Stop()

	mensaje := fmt.Sprintf("HEARTBEAT %s", token)

	for {
		<-ticker.C
		_, err := fmt.Fprint(conn, mensaje)
		if err != nil {
			fmt.Println("[UDP] Error enviando heartbeat:", err)
			break
		}
	}
}
