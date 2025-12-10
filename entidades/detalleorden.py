class DetalleOrden:
    def __init__(self, orden_id, plato_id, cantidad, precio_unitario, id=None):
        self.id = id
        self.orden_id = orden_id
        self.plato_id = plato_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def __repr__(self):
        return f"DetalleOrden(id={self.id}, orden_id={self.orden_id}, cantidad={self.cantidad})"