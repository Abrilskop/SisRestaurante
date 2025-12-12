from servicios.platoService import PlatoService

class PlatoController:
    def __init__(self):
        self.servicio = PlatoService()

    def crear_plato(self, nombre, descripcion, precio):
        # El controlador delega al servicio
        return self.servicio.registrar_plato(nombre, descripcion, precio)