package main

import "fmt"

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
			Cliente(usuario,contraseña)
		
		}else if opcion == 2 {

				ObtenerHistorial()

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