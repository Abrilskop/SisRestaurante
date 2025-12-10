from dao.clienteDAO import ClienteDAO
from dao.platoDAO import PlatoDAO
from entidades.cliente import Cliente

class ClienteService:
    """Lógica de negocio para Clientes, incluyendo la oferta de fidelidad."""

    def __init__(self):
        self.cliente_dao = ClienteDAO()
        self.plato_dao = PlatoDAO()  # Necesario para la oferta

    def registrar_cliente(self, nombre: str, telefono: str) -> Cliente | None:
        """Registra un nuevo cliente."""
        nuevo_cliente = Cliente(nombre, telefono)
        if self.cliente_dao.guardar(nuevo_cliente) != -1:
            return nuevo_cliente
        return None

    def verificar_oferta_fidelidad(self, cliente_id: int, fecha_actual: date) -> bool:
        """
        Verifica si el cliente es elegible para la oferta de piqueo gratis.
        Condición: 4 o más órdenes en los últimos 30 días (un mes).
        """

        return 0

    def obtener_cliente(self, cliente_id: int) -> Cliente | None:
        return self.cliente_dao.buscar_por_id(cliente_id)