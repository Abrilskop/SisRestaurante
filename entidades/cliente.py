# modelo.py
from datetime import date


class Cliente:
    def __init__(self, nombre, telefono, id=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}')"
