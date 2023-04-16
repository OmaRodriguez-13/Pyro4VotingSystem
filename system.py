import Pyro4
import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import *

@Pyro4.expose
class Votacion:
    opciones = []
    def __init__(self):
        self.votos = {}
    
    def registrar_voto(self, candidato):
        if candidato in self.votos:
            self.votos[candidato] += 1
        else:
            self.votos[candidato] = 1
    
    #eliminar
    def eliminar_voto(self, candidato):
        if candidato in self.votos:
            self.votos[candidato] -=1
        else:
            self.votos[candidato] = 1
    
    def contar_votos(self):
        return self.votos
    
    #Establecer y obtener opciones
    @classmethod
    def obtener_opciones(cls):
        return cls.opciones
    
    @classmethod
    def establecer_opciones(cls, opciones):
        cls.opciones = opciones

    #Establecer y obtener tema
    @classmethod
    def obtener_tema(cls):
        return cls.tema 
    
    @classmethod
    def establecer_tema(cls, tema):
        cls.tema = tema
    

#ip = Pyro4.socketutil.getInterfaceAddress("192.168.1.103")
ip = socket.gethostbyname(socket.gethostname())

daemon = Pyro4.Daemon(host=ip)

votacion = Votacion()
uri = daemon.register(votacion, objectId='votacion')

tema = simpledialog.askstring("Tema de la votación", "Ingrese el tema de la votación: ")

messagebox.showinfo("URI del SERVIDOR", f"Servidor listo. URI= {uri}")
print("Servidor listo. URI= ", uri)

# Obtener opciones del usuario
opciones = []
while True:
    num_opciones = simpledialog.askinteger("Votación", "Ingrese el número de opciones para la votación:")
    for i in range(num_opciones):
        opcion = simpledialog.askstring("Ingresando opciones...", f"Ingrese la opción {i+1}:")
        opciones.append(opcion)
    confirmacion = messagebox.askquestion("Confirmación", "¿Desea agregar más opciones?")
    if confirmacion == "no":
        break

# Establecer opciones y tema en el servidor
Votacion.establecer_opciones(opciones)
Votacion.establecer_tema(tema)

daemon.requestLoop()