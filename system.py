import Pyro4

@Pyro4.expose
class Votacion:
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

daemon = Pyro4.Daemon()
uri = daemon.register(Votacion())
ns = Pyro4.locateNS()
ns.register('obj', uri)

print("Servidor listo. URI =", uri)
daemon.requestLoop()