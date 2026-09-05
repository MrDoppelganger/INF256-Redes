package main

import (
    "bufio"
    "fmt"
    "net"
    "os"
)

func IniciarChatTCP() {
    host := "127.0.0.1"
    port := "9000" // Cambiado al puerto TCP
    conn, err := net.Dial("tcp", host+":"+port)

    if err != nil {
        fmt.Println("Error conectando al chat:", err)
        return
    }
    defer conn.Close()

    fmt.Println("Conectado al servidor TCP. Ingresa comando (ej: LOGIN user pass):")
    reader := bufio.NewReader(os.Stdin)
    texto, err := reader.ReadString('\n')
    if err != nil {
        fmt.Println(err)
        return
    }

    fmt.Fprint(conn, texto)
    
    // Leer respuesta del servidor
    respuesta, _ := bufio.NewReader(conn).ReadString('\n')
    fmt.Print("Servidor responde: ", respuesta)
}