from servicios.ordenService import OrdenService

class OrdenController:
    def __init__(self):
        self.servicio = OrdenService()

    def crear_orden(self, cliente_id, tipo, total):
        return self.servicio.registrar_orden(cliente_id, tipo, total)