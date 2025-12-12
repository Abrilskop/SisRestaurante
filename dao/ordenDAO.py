from dao.conexion import DBConnection
from entidades.orden import Orden

class OrdenDAO:
    def guardar(self, orden: Orden) -> int:
        conn = DBConnection.get_connection()
        if not conn: return -1
        cursor = conn.cursor()
        sql = "INSERT INTO orden (cliente_id, fecha, tipo_orden, total) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(sql, (orden.cliente_id, orden.fecha, orden.tipo_orden, orden.total))
            conn.commit()
            orden.id = cursor.lastrowid
            return orden.id
        except Exception as e:
            print(f"Error OrdenDAO: {e}")
            return -1
        finally:
            cursor.close()
            conn.close()
            
    # Este método lo usaremos en el siguiente ejercicio (Fidelidad),
    # pero es mejor dejarlo creado de una vez en el DAO.
    def contar_ordenes_ultimo_mes(self, cliente_id, fecha_limite):
        conn = DBConnection.get_connection()
        if not conn: return 0
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM orden WHERE cliente_id = %s AND fecha >= %s"
        try:
            cursor.execute(sql, (cliente_id, fecha_limite))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except Exception:
            return 0
        finally:
            cursor.close()
            conn.close()