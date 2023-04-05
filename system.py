import Pyro4

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
     
    def establecer_tema(self, tema):
        self.tema = tema
    
    def obtener_tema(self):
        return self.tema

# Obtener la dirección IP del servidor
direccion_ip = Pyro4.socketutil.getInterfaceAddress(input("Ingrese la ip: "))
daemon = Pyro4.Daemon(host=direccion_ip)
#daemon = Pyro4.Daemon()
uri = daemon.register(Votacion(), objectId="obj")
ns = Pyro4.locateNS()
ns.register('obj', uri)

print("Servidor listo. URI =", uri)

# Obtener opciones del usuario
opciones = []
while True:
    num_opciones = int(input("Ingrese el número de opciones para la votación: "))
    for i in range(num_opciones):
        opcion = input(f"Ingrese la opción {i+1}: ")
        opciones.append(opcion)
    confirmacion = input("¿Desea agregar más opciones? (s/n): ")
    if confirmacion.lower() == "n":
        break

# Establecer opciones y tema en el servidor
Votacion.establecer_opciones(opciones)

daemon.requestLoop()