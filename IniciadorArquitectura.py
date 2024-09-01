import subprocess
import math

def main():
    N = int(input("Ingresa la cantidad de nodos de su arquitecura: "))
    while((math.log(N,2)%1!=0 or N>8)or N<1):
        N = int(input("La cantidad de nodos debe ser exponente de 2 y como maximo 8: "))
    puertoBase = 5001  

    nodos = []

    #Generar configuración de puertos para cada nodo
    for i in range(N):
        puerto_escucha = puertoBase + i
        puerto_izquierda = puertoBase + (i - 1) % N  # Calcula el puerto de la izquierda
        puerto_derecha = puertoBase + (i + 1) % N    # Calcula el puerto de la derecha
        nodos.append((puerto_escucha, puerto_izquierda, puerto_derecha))

    #Ejecutar cada nodo en una nueva ventana de cmd
    for nodo in nodos:
        puerto_escucha, puerto_izquierda, puerto_derecha = nodo
        subprocess.Popen(['cmd', '/c', 'start', 'python', 'nodo.py', 
                          str(puerto_escucha), 
                          str(puerto_izquierda), 
                          str(puerto_derecha)],
                          creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    main()
