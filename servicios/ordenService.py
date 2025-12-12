from datetime import date
from dao.ordenDAO import OrdenDAO
from entidades.orden import Orden

class OrdenService:
    def __init__(self):
        self.dao = OrdenDAO()

    def registrar_orden(self, cliente_id, tipo, total):
        nueva_orden = Orden(cliente_id, date.today(), tipo, total)
        id_gen = self.dao.guardar(nueva_orden)
        
        if id_gen != -1:
            nueva_orden.id = id_gen 
            return nueva_orden
        return None