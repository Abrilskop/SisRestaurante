from datetime import date, timedelta # <--- Importante: timedelta
from dao.clienteDAO import ClienteDAO
from dao.platoDAO import PlatoDAO
from dao.ordenDAO import OrdenDAO    # <--- Importante: OrdenDAO
from entidades.cliente import Cliente

class ClienteService:
    """Lógica de negocio para Clientes, incluyendo la oferta de fidelidad."""

    def __init__(self):
        self.cliente_dao = ClienteDAO()
        self.plato_dao = PlatoDAO()
        self.orden_dao = OrdenDAO()  # <--- Inicializamos el DAO de Orden

    def registrar_cliente(self, nombre: str, telefono: str) -> Cliente | None:
        nuevo_cliente = Cliente(nombre, telefono)
        if self.cliente_dao.guardar(nuevo_cliente) != -1:
            return nuevo_cliente
        return None

    def verificar_oferta_fidelidad(self, cliente_id: int) -> bool:
        """
        Verifica si el cliente es elegible para la oferta.
        Regla: 4 o más órdenes en los últimos 30 días.
        """
        # 1. Calcular la fecha de hace 30 días
        fecha_limite = date.today() - timedelta(days=30)
        
        # 2. Preguntar al DAO cuántas órdenes tiene desde esa fecha
        cantidad = self.orden_dao.contar_ordenes_ultimo_mes(cliente_id, fecha_limite)
        
        # 3. Aplicar la regla de negocio
        return cantidad >= 4

    def obtener_cliente(self, cliente_id: int) -> Cliente | None:
        return self.cliente_dao.buscar_por_id(cliente_id)