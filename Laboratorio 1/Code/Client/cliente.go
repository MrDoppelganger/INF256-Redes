package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	host := "127.0.0.1"
	port := "8080"
	conn, err := net.Dial("tcp", host+":"+port)

	if err != nil {
		fmt.Println(err)
		return
	}
	defer conn.Close()

	//lo saque de un video de un chino que habla espanol
	fmt.Println("ingrese peticion")
	reader := bufio.NewReader(os.Stdin)
	texto, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println(err)
	}

	fmt.Fprint(conn, texto)

}
