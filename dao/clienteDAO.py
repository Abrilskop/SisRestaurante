from dao.conexion import DBConnection
from entidades.cliente import Cliente

class ClienteDAO:
    """DAO para la entidad Cliente."""

    def guardar(self, cliente: Cliente) -> int:
        conn = DBConnection.get_connection()
        if not conn: return -1
        cursor = conn.cursor()
        sql = "INSERT INTO cliente (nombre, telefono) VALUES (%s, %s)"
        try:
            cursor.execute(sql, (cliente.nombre, cliente.telefono))
            conn.commit()
            cliente.id = cursor.lastrowid
            return cliente.id
        except DBConnection.error as err:
            raise(err)
        finally:
            cursor.close()
            conn.close()

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        conn = DBConnection.get_connection()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id, nombre, telefono FROM cliente WHERE id = %s"
        try:
            cursor.execute(sql, (cliente_id,))
            resultado = cursor.fetchone()
            if resultado:
                return Cliente(id=resultado['id'], nombre=resultado['nombre'], telefono=resultado['telefono'])
            return None
        except DBConnection.error as err:
            raise(err)
        finally:
            cursor.close()
            conn.close()