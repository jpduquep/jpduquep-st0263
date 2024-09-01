import grpc
from concurrent import futures
import time
import threading
import json
import claveunica

import document_pb2
import document_pb2_grpc

class DocumentServiceServicer(document_pb2_grpc.DocumentServiceServicer):
    
    def __init__(self):
        self.listaDocumentos = [("titulo", "informacion")]


    def cargarDocumento(self, request,context):
        
        cantidadNodos = int(request.cantidadNodos)
        puertoEscucha = int(request.puertoEscucha)
        resultado = claveunica.clave(int(cantidadNodos),request.titulo)[1]
        
        #Verificamos que nosotros si seamos los responsable de guardar este documento sino hay que seguirlo rotando
        if int(resultado) == int(puertoEscucha) - 5001:
            self.listaDocumentos.append((request.titulo, request.contenido))
            return document_pb2.uploadResponse(mensajeRespuesta="Documento guardado correctamente.",idRemitente = request.idRemitente)
        else:
            #Hay que rotar la solicitud hacia la derecha para encontrar
            if (cantidadNodos + 5000) == puertoEscucha:
                nuevaRequest = document_pb2.uploadRequest(
                    idRemitente=request.idRemitente,
                    titulo=request.titulo,
                    contenido=request.contenido,
                    cantidadNodos = str(request.cantidadNodos),
                    puertoEscucha = str(5001)
                )
                with grpc.insecure_channel(f'localhost:{5001}') as canalSiguiente:
                    stubSiguiente = document_pb2_grpc.DocumentServiceStub(canalSiguiente)
                    
                    return stubSiguiente.cargarDocumento(nuevaRequest)
            else:
                nuevaRequest = document_pb2.uploadRequest(
                    idRemitente=request.idRemitente,
                    titulo=request.titulo,
                    contenido=request.contenido,
                    cantidadNodos = str(request.cantidadNodos),
                    puertoEscucha = str(int(request.puertoEscucha) + 1)
                )
                with grpc.insecure_channel(f'localhost:{int(puertoEscucha)+1}') as canalSiguiente:
                    stubSiguiente = document_pb2_grpc.DocumentServiceStub(canalSiguiente)
                    return stubSiguiente.cargarDocumento(nuevaRequest)

    def descargarDocumento(self,request,conext):

        cantidadNodos = int(request.cantidadNodos)
        puertoEscucha = int(request.puertoEscucha)
        resultado = claveunica.clave(cantidadNodos,request.titulo)[1]

        #Verificamos que nosotros seamos el nodo correspondiente a donde deberia estar el archivo guardado
        if int(resultado) == int(puertoEscucha) - 5001:
            for tituloLocal, informacionLocal in self.listaDocumentos:
                if tituloLocal == request.titulo:
                    return document_pb2.downloadResponse(idRemitente = request.idRemitente,titulo = tituloLocal,contenido = informacionLocal)
            return document_pb2.downloadResponse(idRemitente = request.idRemitente,titulo = tituloLocal,contenido = "El contenido vinculado a este titulo no existe")
        else:
            #Hay que seguir la solicitud hacia la izquierda
            if str(int(cantidadNodos) + 5000) == str(puertoEscucha):
                nuevaRequest = document_pb2.downloadRequest(
                    idRemitente=request.idRemitente,
                    titulo=request.titulo,
                    cantidadNodos = str(request.cantidadNodos),
                    puertoEscucha = str(5001)
                )
                with grpc.insecure_channel(f'localhost:{5001}') as canalSiguiente:
                    stubSiguiente = document_pb2_grpc.DocumentServiceStub(canalSiguiente)
                    return stubSiguiente.descargarDocumento(nuevaRequest)
            else:
                nuevaRequest = document_pb2.downloadRequest(
                    idRemitente=request.idRemitente,
                    titulo=request.titulo,
                    cantidadNodos = str(request.cantidadNodos),
                    puertoEscucha = str(int(request.puertoEscucha) + 1)
                )
                with grpc.insecure_channel(f'localhost:{int(puertoEscucha)+1}') as canalSiguiente:
                    stubSiguiente = document_pb2_grpc.DocumentServiceStub(canalSiguiente)
                    return stubSiguiente.descargarDocumento(nuevaRequest)
    
    def listarRecursos(self,request,conext):

        cantidadNodos = int(request.cantidadNodos)
        puertoEscucha = int(request.puertoEscucha)
    
        if int(request.idDestinatario) == (int(puertoEscucha)-5001):
            listaDocumentos = [
                document_pb2.Documento(titulo=doc[0], contenido=doc[1])
                for doc in self.listaDocumentos
            ]
            return document_pb2.listResponse(idRemitente = request.idRemitente,documentos = listaDocumentos)
        
        else:
            #Hay que seguir la solicitud hacia la izquierda
            if (cantidadNodos + 5000) == puertoEscucha:
                nuevaRequest = document_pb2.listRequest(
                    idRemitente=request.idRemitente,
                    idDestinatario = request.idDestinatario,
                    cantidadNodos = str(request.cantidadNodos),
                    puertoEscucha = str(5001)
                )
                with grpc.insecure_channel(f'localhost:{5001}') as canalSiguiente:
                    stubSiguiente = document_pb2_grpc.DocumentServiceStub(canalSiguiente)
                    return stubSiguiente.listarRecursos(nuevaRequest)
            else:
                nuevaRequest = document_pb2.listRequest(
                    idRemitente=request.idRemitente,
                    idDestinatario = request.idDestinatario,
                    cantidadNodos = str(request.cantidadNodos),
                    puertoEscucha = str(int(request.puertoEscucha) + 1)
                )
                with grpc.insecure_channel(f'localhost:{int(puertoEscucha)+1}') as canalSiguiente:
                    stubSiguiente = document_pb2_grpc.DocumentServiceStub(canalSiguiente)
                    return stubSiguiente.listarRecursos(nuevaRequest)


def serve(puerto):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    document_pb2_grpc.add_DocumentServiceServicer_to_server(DocumentServiceServicer(), server)
    server.add_insecure_port(f'[::]:{puerto}')
    server.start()
    print("Servidor gRPC en ejecución en el puerto",puerto,"...")
    print("Soy el nodo",puerto-5001)
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

def enviarMensajes(puertoIzq, puertoDer, puertoDeEscucha,cantidadNodos):
    idNodo = int(puertoDeEscucha) - 5001
    '''
    print("pIzq",puertoIzq)
    print("pDer",puertoDer)
    print("pEscucha",puertoDeEscucha)
    '''
    with grpc.insecure_channel(f'localhost:{puertoIzq}') as canal_grpc_Izq, grpc.insecure_channel(f'localhost:{puertoDer}') as canal_grpc_Der:
        stubIzquierda = document_pb2_grpc.DocumentServiceStub(canal_grpc_Izq)
        stubDerecha = document_pb2_grpc.DocumentServiceStub(canal_grpc_Der)

        while True:
            resp = input('\nDigite salir si desea terminar la consola \n1: Para cargar un documento \n2: Para descargar un documento\n3: Mostrar lista de documentos\nR/ ')
            if resp.lower() == "salir":
                break

            elif resp == '1':  # Cargar documento a la red
                titulo = input("Digita el nombre del documento que vas a ingresar: ")
                mensaje = input("Cuál es el contenido: ")

                request = document_pb2.uploadRequest(
                    idRemitente=str(idNodo),
                    titulo=titulo,
                    contenido=mensaje,
                    cantidadNodos = str(cantidadNodos),
                    puertoEscucha = str(puertoDer)
                )

                #Lanza solicitud
                response = stubDerecha.cargarDocumento(request)
                print("Respuesta:", response.mensajeRespuesta)

            elif resp == '2':  # Descargar documento de la red
                titulo = input("Digita el nombre del documento que buscas con extensión: ")
                request = document_pb2.downloadRequest(
                    idRemitente=str(idNodo),
                    titulo=titulo,
                    cantidadNodos = str(cantidadNodos),
                    puertoEscucha = str(puertoDer)
                )
                response = stubDerecha.descargarDocumento(request)
                print("Titulo:",response.titulo,"\n"+response.contenido)

            elif resp == '3':  # Mostrar listado
                nodoConsultar = input("Que nodo quieres que rote la lista: ")

                request = document_pb2.listRequest(
                    idRemitente=str(idNodo),
                    idDestinatario = str(nodoConsultar),
                    cantidadNodos = str(cantidadNodos),
                    puertoEscucha = str(puertoDer)
                )
                response = stubDerecha.listarRecursos(request)
                print("\nListado de documentos del nodo",nodoConsultar)
                print("-" * 20)
                for documento in response.documentos:
                    print("Titulo:", documento.titulo)
                    print("Informacion:",documento.contenido)
                    print("-" * 20)
                print("\n")

def iniciarNodo(puertoDeEscucha, puertoIzq, puertoDer,cantidadNodos):
    # Iniciar el servidor gRPC en un hilo separado
    threading.Thread(target=serve, args=(puertoDeEscucha,)).start()
    time.sleep(3)

    # Iniciar la función para enviar mensajes
    enviarMensajes(puertoIzq, puertoDer, puertoDeEscucha,cantidadNodos)

if __name__ == '__main__':
    import sys
    puertoDeEscucha = int(sys.argv[1])
    puertoIzq = int(sys.argv[2])
    puertoDer = int(sys.argv[3])
    cantidadNodos = int(sys.argv[4])

    iniciarNodo(puertoDeEscucha, puertoIzq, puertoDer,cantidadNodos)
