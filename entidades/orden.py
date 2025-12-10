class Orden:
    # Tipos de orden: I=Individual, C=Colectiva, F=Familiar
    TIPO_ORDEN = {'I', 'C', 'F'}

    def __init__(self, cliente_id, fecha, tipo_orden, total, id=None):
        self.id = id
        self.cliente_id = cliente_id
        self.fecha = fecha  # Usar datetime.date o datetime.datetime
        self.tipo_orden = tipo_orden if tipo_orden in self.TIPO_ORDEN else 'I'
        self.total = total  # Decimal o Float

    def __repr__(self):
        return f"Orden(id={self.id}, cliente_id={self.cliente_id}, tipo='{self.tipo_orden}')"