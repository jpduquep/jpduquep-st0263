# Proyecto Reto 1 - Implementación de Sistema Peer-to-Peer (P2P)

## Estudiantes
- **Nombre:** Juan Pablo Duque  
  **Correo Electrónico:** [jpduquep@eafit.edu.co](mailto:jpduquep@eafit.edu.co)
- **Nombre:** Jaime Uribe  
  **Correo Electrónico:** [jruribem@eafit.edu.co](mailto:jruribem@eafit.edu.co)

## Profesor
- **Nombre:** Álvaro Enrique Ospina Sanjuan  
  **Correo Electrónico:** [aeospinas@eafit.edu.co](mailto:aeospinas@eafit.edu.co)

## Descripción
Este reto número 1 consiste en la implementación de un sistema Peer-to-Peer (P2P) que realiza la comunicación mediante RPC y API REST. El objetivo principal es que cada nodo tenga la capacidad de actuar como cliente y servidor, compartiendo información con otros peers sin la necesidad de un servidor central. Además, para mejorar la eficiencia en la localización de los archivos, se utiliza una tabla hash simple.

## Aspectos Cumplidos
El proyecto logró implementar con éxito la comunicación híbrida utilizando gRPC y API REST, lo que permitió un manejo eficiente y escalable de las operaciones entre los nodos de la red P2P. Además, se implementó una asignación descentralizada de archivos, donde cada nodo es responsable de almacenar y gestionar sus propios recursos sin dependencia de un servidor central.

Se implementó correctamente un algoritmo de identificador único tipo hash, que asigna a cada archivo un identificador basado en su contenido o nombre. Este identificador se almacena en una tabla hash en cada nodo, permitiendo una búsqueda rápida y eficiente de archivos en la red. Así, el proyecto cumplió con los objetivos de descentralización, comunicación efectiva y gestión eficiente de archivos en una red P2P no estructurada.

## Aspectos No Cumplidos
Aunque el proyecto cumplió con la mayoría de los requerimientos, hay algunos aspectos que no se lograron:
- No se realizó el despliegue en AWS Academy.
- No se implementó un nivel de seguridad adecuado para el proyecto.

## Información General

### Arquitectura
![image](https://github.com/user-attachments/assets/f77e4269-aff0-42d4-9b3d-35809cdf8cfa)


### Información general
En el proyecto se implementó gRPC, el framework de llamada a procedimiento remoto (RPC) desarrollado por Google, utilizando librerías de Python para manejar la comunicación interna entre microservicios en cada nodo de la red P2P. gRPC se basa en la definición de servicios en un archivo `.proto`, que actúa como un contrato entre el cliente y el servidor. En este archivo `.proto`, se definen las funciones disponibles para la llamada remota, especificando tanto los mensajes de solicitud (`request`) como los de respuesta (`response`). Esta estructura permite una comunicación eficiente y de alto rendimiento entre los microservicios, y es independiente del lenguaje de programación, lo que facilita la integración con otros servicios o sistemas que puedan estar implementados en diferentes tecnologías.

### Patrones
- **Singleton:** En la implementación del servidor gRPC, el objeto `DocumentServiceServicer` sigue un patrón Singleton, ya que se instancia una sola vez y maneja todas las solicitudes gRPC entrantes en un único proceso.
- **Facade:** La estructura del servicio gRPC actúa como una fachada, simplificando la complejidad de las interacciones subyacentes y exponiendo una API clara y sencilla para los clientes que desean interactuar con el servicio.

### Mejores Prácticas Utilizadas
- **gRPC:** La elección de gRPC para manejar la comunicación entre nodos permite una transmisión eficiente de datos y asegura una baja latencia en las operaciones distribuidas.
- **Separación de responsabilidades:** El código sigue la práctica de separar claramente las responsabilidades, donde cada función y clase tiene un propósito específico, como `DocumentServiceServicer` para manejar la lógica del servicio y `main()` para configurar y ejecutar los nodos.
- **Concurrencia:** El servidor gRPC se ejecuta utilizando un `ThreadPoolExecutor`, lo que permite manejar múltiples solicitudes concurrentes de manera eficiente.
- **Comentarios en el código:** El código incluye comentarios útiles que explican la lógica detrás de ciertos bloques.

## Entorno de Desarrollo y Configuraciones

### IDE
- **Visual Studio Code**

### Lenguaje de Programación
- **Python v3.11.6**

### Librerías y Paquetes
- `grpcio v1.66.1`
- `grpc-tools v1.66.1`
- `subprocess`
- `threading`
- `math`

### Instalación de Librerías
Para instalar las librerías necesarias, ejecuta el siguiente comando en una terminal:
'pip install grpcio grpcio-tools'

### Ejecucón
El archivo .proto requiere correr el siguiente comando para crear los archivos necesarios para poder funcionar. Se sugiere utilizar el nombre del archivo pues las importaciones tienen el nombre de este archivo más el agregado automático para correr el comando.
`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. document.proto`

 Una vez ejecutado ese comnado, se debe ejecutar la siguiente línea para iniciar los nodos. Esto abrirá múltiples ventanas de consola, cada una representa un nodo diferente
 `python main.py`

Durante la ejecución, el script te pedirá que ingreses la cantidad de nodos que deseas crear. Asegúrate de que este número sea una potencia de 2 (e.g., 2, 4, 8).

Interactuar con los Nodos:
En cada consola abierta, puedes interactuar con el nodo correspondiente. Elige entre las siguientes opciones:
1: Para cargar un documento en la red.
2: Para descargar un documento desde la red.
3: Para mostrar la lista de documentos almacenados en un nodo específico.


### Imagenes

![image](https://github.com/user-attachments/assets/352f9705-8dc1-4625-89e3-dd1818af208a)
![image](https://github.com/user-attachments/assets/a50b29aa-3f54-43cd-ad2d-757c84ec7624)






