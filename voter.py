import Pyro4
import tkinter as tk

class Interfaz:
    def __init__(self, uri):
        self.votacion = Pyro4.Proxy(uri)
        self.root = tk.Tk()
        self.root.title("Sistema de votación")
        self.root.iconbitmap('urna.ico')
        self.root.geometry('250x150')
        self.num_opciones = int(input("Ingrese el número de opciones para la votación: "))
        self.candidatos = []
        for i in range(self.num_opciones):
            opcion = input(f"Ingrese la opción {i+1}: ")
            self.candidatos.append(opcion)
        self.seleccion = tk.StringVar()
        self.seleccion.set(self.candidatos[0])
        self.opciones = tk.OptionMenu(self.root, self.seleccion, *self.candidatos)
        self.opciones.grid(row=0, column=4)
        self.boton_votar = tk.Button(self.root, text="Votar", command=self.registrar_voto)
        self.boton_votar.grid(row=1, column=3)
        self.boton_votarE = tk.Button(self.root, text="Eliminar Voto", command=self.eliminar_voto)
        self.boton_votarE.grid(row=1, column=5)
        self.boton_votarA = tk.Button(self.root, text="Actualizar votos", command=self.actualizar_resultados)
        self.boton_votarA.grid(row=2, column=4)
        self.resultados = tk.Label(self.root, text="")
        self.resultados.grid(row=3, column=4)
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

ns = Pyro4.locateNS()
uri = ns.lookup('obj')

interfaz = Interfaz(uri)
interfaz.iniciar()