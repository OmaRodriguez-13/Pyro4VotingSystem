import Pyro4
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import *

class Interfaz:
    def __init__(self, uri):
        self.votacion = Pyro4.Proxy(uri)
        self.root = tk.Tk()
        self.root.title("Sistema de votación")
        self.root.iconbitmap('urna.ico')
        self.root.geometry('390x500')

        # Hacer que la ventana no sea redimensionable
        self.root.resizable(False, False)


        self.Ltema = tk.Label(self.root, text="Tema:", font=("Courier New", 12))
        self.Ltema.grid(row=0, column=2, pady=10)

        
         # Obtener opciones y tema del servidor
        self.candidatos = self.votacion.obtener_opciones()
        self.temav = self.votacion.obtener_tema()
        
        self.seleccion = tk.StringVar()
        self.seleccion.set(self.candidatos[0])

        self.opciones = tk.OptionMenu(self.root, self.seleccion, *self.candidatos)
        self.opciones.grid(row=1, column=2)

        self.boton_votar = tk.Button(self.root, text="Votar", command=self.registrar_voto, width=8)
        self.boton_votar.grid(row=2, column=1, padx=20, pady=10)

        self.boton_votarE = tk.Button(self.root, text="Eliminar Voto", command=self.eliminar_voto, width=12)
        self.boton_votarE.grid(row=2, column=3, padx=20, pady=10)

        self.boton_votarA = tk.Button(self.root, text="Actualizar votos", command=self.actualizar_resultados, width=20)
        self.boton_votarA.grid(row=3, column=2, pady=10)


        self.resultados = tk.Label(self.root, text="", font=("Courier New", 11))
        self.resultados.grid(row=4, column=2, pady=10)

        self.Ltema.config(text="Tema: " + self.temav)
        self.actualizar_resultados()

    def registrar_voto(self):
        candidato = self.seleccion.get()
        self.votacion.registrar_voto(candidato)
        self.actualizar_resultados()

    def eliminar_voto(self):
        candidato = self.seleccion.get()
        self.votacion.eliminar_voto(candidato)
        self.actualizar_resultados()
    
    def actualizar_resultados(self):
        votos = self.votacion.contar_votos()
        texto = ""
        for candidato in self.candidatos:
            if candidato in votos:
                texto += f"{candidato}: {votos[candidato]} votos\n"
            else:
                texto += f"{candidato}: 0 votos\n"
        self.resultados.config(text=texto)
    
    def iniciar(self):
        self.root.mainloop()


server_ip = simpledialog.askstring(
    "Dirección IP del servidor", "Ingrese la dirección IP del servidor:")
if server_ip is None:
    # Si el usuario cancela el diálogo, salir del programa
    exit()

server_port = simpledialog.askstring(
    "Dirección IP del servidor", "Ingrese el puerto del servidor:")
if server_ip is None:
    # Si el usuario cancela el diálogo, salir del programa
    exit()
#obj = input("Introduzca lo que falta: ")

#uri = "PYRO:votacion@{obj}"
uri = f"PYRO:votacion@{server_ip}:{server_port}"

messagebox.showinfo( "URI del SERVIDOR", uri)
#uri = input("Introduzca la URI del servidor: ")

interfaz = Interfaz(uri)
interfaz.iniciar()