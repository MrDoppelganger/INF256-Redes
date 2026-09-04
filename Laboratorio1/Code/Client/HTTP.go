package main

import (
	"bufio"
	"fmt"
	"net"
	"encoding/json"
)


func cliente(usuario string, contraseña string){
	port := "8080"
	host := "127.0.0.1"
	c, err := net.Dial("tcp", host+":"+port)
	
	if err != nil {
		fmt.Println(err)
		return
	}
	postBody, _ := json.Marshal(map[string]string{"Username":usuario,"Password":contraseña,})
	request := "POST /register HTTP/1.1\r\n"
	request += "Host: 127.0.0.1:8080\r\n "
	request += "Content-Type: application/json\r\n"
	request += fmt.Sprintf("Content-Length: %d\r\n", len(postBody))
	request += "Connection: close\r\n"
	request += "\r\n"
	request += string(postBody)
	
	_, err = c.Write([]byte(request))
	if err != nil {
		fmt.Println(err)
		return
	}
	reader := bufio.NewReader(c)
	for {
		linea, err := reader.ReadString('\n')
		if err != nil {
			break
		}

		fmt.Print(linea)
	}
}

func obtenerHistorial() {
	host := "127.0.0.1"
	port := "8080"

	conn, err := net.Dial("tcp", host+":"+port)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer conn.Close()

	request := "GET /history HTTP/1.1\r\n"
	request += "Host: 127.0.0.1:8080\r\n"
	request += "Connection: close\r\n"
	request += "\r\n"

	_, err = conn.Write([]byte(request))
	if err != nil {
		fmt.Println(err)
		return
	}

	reader := bufio.NewReader(conn)

	fmt.Println("\nRespuesta del servidor:")

	for {
		linea, err := reader.ReadString('\n')

		if linea != "" {
			fmt.Print(linea)
		}

		if err != nil {
			break
		}
	}
}

	
	



func main(){
	for {
		var opcion int
		fmt.Println("\n--- MENU ---")
		fmt.Println("1. Registrar usuario")
		fmt.Println("2. Ver historial")
		fmt.Println("3. Salir")
		fmt.Print("Seleccione una opcion: ")
		fmt.Scanln(&opcion)
		if opcion == 1{
			var usuario string
			var contraseña string
			fmt.Print("Ingresa tu usuario: ")
			fmt.Scanln(&usuario)
			fmt.Print("Ingresa tu contraseña: ")
			fmt.Scanln(&contraseña)
			cliente(usuario,contraseña)
		
		}else if opcion == 2 {

				obtenerHistorial()

		}else if opcion == 3 {

				fmt.Println("Saliendo...")
				break

		}else if opcion == 3 {

				fmt.Println("Saliendo...")
				break

		}else {

			fmt.Println("Opcion invalida")
		}

	}
		
		
}
