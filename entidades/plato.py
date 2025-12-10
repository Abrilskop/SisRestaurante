class Plato:
    def __init__(self, nombre, descripcion, precio, id=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio  # Decimal o Float

    def __repr__(self):
        return f"Plato(id={self.id}, nombre='{self.nombre}', precio={self.precio})"