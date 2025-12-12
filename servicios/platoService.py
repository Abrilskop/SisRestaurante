from dao.platoDAO import PlatoDAO
from entidades.plato import Plato

class PlatoService:
    def __init__(self):
        self.dao = PlatoDAO()

    def registrar_plato(self, nombre, descripcion, precio):
        nuevo_plato = Plato(nombre, descripcion, precio)
        id_generado = self.dao.guardar(nuevo_plato)
        
        if id_generado != -1:
            nuevo_plato.id = id_generado 
            return nuevo_plato
        return None