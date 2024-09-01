import math
import re  #Esto es para expresiones regulares para limpiar cadenas
abecedario = {
    'A': 1, 'a': 1,
    'B': 2, 'b': 2,
    'C': 3, 'c': 3,
    'D': 4, 'd': 4,
    'E': 5, 'e': 5,
    'F': 6, 'f': 6,
    'G': 7, 'g': 7,
    'H': 8, 'h': 8,
    'I': 9, 'i': 9,
    'J': 10, 'j': 10,
    'K': 11, 'k': 11,
    'L': 12, 'l': 12,
    'M': 13, 'm': 13,
    'N': 14, 'n': 14,
    'O': 15, 'o': 15,
    'P': 16, 'p': 16,
    'Q': 17, 'q': 17,
    'R': 18, 'r': 18,
    'S': 19, 's': 19,
    'T': 20, 't': 20,
    'U': 21, 'u': 21,
    'V': 22, 'v': 22,
    'W': 23, 'w': 23,
    'X': 24, 'x': 24,
    'Y': 25, 'y': 25,
    'Z': 26, 'z': 26,
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9
}

def volteo(n):
    if(n == "0"):
        return "1"
    else:
        return "0"
    
def limpiarTitulo(titulo):
    return re.sub(r'[^a-zA-Z0-9]','',titulo)

def convertirBinaNumero(cadenaBinaria):
    largo = len(cadenaBinaria)
    sumaNumero = 0
    for a in range(largo):
        exp = 2**abs(largo-a-1)
        if (cadenaBinaria[a] == '1'):
            sumaNumero += int(exp)
    return sumaNumero

        
def clave(N, titulo): #N es numero de nodos en el P2P
    if (math.log(N,2)%1==0): #Verificamos que la cantidad de nodos es un exponente de 2
        cantidadBits = int(math.log(N,2))
        cadenaBits = ['0']*cantidadBits
        titulo = limpiarTitulo(str(titulo))

        #print("El titulo limpio es:",titulo)
        #print("La cadena a hacer la clave es",cadenaBits)

        #Proceso de armado de cadena
        for letra in titulo:
            #print("Letra: ",letra)
            bitSelecto = int(abecedario[str(letra)])%cantidadBits
            #print("El bit que tiene cambio por la letra/digito",letra,abecedario[letra],"es",bitSelecto)
            cadenaBits[bitSelecto] = str(volteo(cadenaBits[bitSelecto]))
        cadenaBinaria = ''.join(cadenaBits)
        numero = convertirBinaNumero(cadenaBinaria)
        return (cadenaBinaria,numero)
    else:
        return False #esto retorna en caso de que no sea un exponente de 2 la cantidad de nodos que hay
    
'''
def main():
    numeroNodos = int(input("Cuantos nodos tiene el sistema? "))
    nombreArchivo = input("Que es lo que estas buscando? ")
    print("la clave final es:",clave(numeroNodos,nombreArchivo))

if __name__ == "__main__":
    main()
'''