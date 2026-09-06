
---

> **Universidad:** Universidad Técnica Federico Santa María (UTFSM)  
> **Curso:** Redes de computadores [INF256] — 2° Semestre/2026  
> **Fecha:** Agosto, 2026  
>
> **Integrantes:**
> * Vicente Rodríguez Rogers | 21.303.222-4 | 202273503-1 
> * Nicolás Muñoz | 21.270.184-K | 202273641-0 
> * Diego Octavio Espinoza | 21.221.834-0 | 202273576-7
> **Grupo 9**

---

## 🛠️ Herramientas Utilizadas

* **Control de Versiones:** GitHub
* **Editor:** Visual Studio Code
* **Lenguaje**: Pyhton, go

## 💻 Ambientes de Ejecución

* **Sistemas Operativos:** 
    * Windows 11
    * Ubuntu 22.04.5 LTS
## 🧱 Estructura del repositorio

```bash
├── Code/
│   ├── Client
│   │    ├── client_http.go
│   │    ├── client_tcp.go
│   │    ├── client_udp.go
│   │    ├── go.mod
│   │    └── main.go
│   ├── Server
│   │    ├── data
│   │    │    ├── historial.csv
│   │    │    ├── sesiones.csv
│   │    │    └── usuarios.csv
│   │    ├── server_http.py
│   │    ├── server_tcp.py
│   │    ├── server_udp.py
│   │    ├── storage.py
│   │    ├── watchdog.py
│   │    └── main.py
├── Docs/
│   └── Lab_1_redes_2026_2.pdf
├── .gitignore
└── README.md
```
    
## 🚀 Instrucciones de Ejecución
**Previo:**
*   Se requiere tener instalado python 3.1 y Go 1.2 o compatibles.
*   Los archivos *.csv* pueden estar vacios al iniciar o con datos pero si o si deben existir
    los 3.
**Despliegue del Servidor:**
*   Abrir una terminal posicionada en la carpeta *Code/Server*
*   Ejecutar el comando ```python3 main.py```
**Ejecucion del Cliente:**
*   Abrir una terminal posicionada en la carpeta *Code/Client*
*   Ejecutar el comando ```go run .```
*   Interactuar con el menu.
## ⚠️ Consideraciones
*   Se asume que el usuario simpre colocara inputs validos
*   Se asume que durante el Login, solo sera necesario verificar el estado de *"Actividad" de
    la sesion, el encargado de revisar y expirar este estado sera el watchdog
*   Se debe de correr primero el server y luego los clientes
