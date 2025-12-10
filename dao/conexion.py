# dao.py
import mysql.connector
from mysql.connector import errorcode
from datetime import date

from configuracion.config import DB_CONFIG


class DBConnection:

    error=None

    @staticmethod
    def get_connection():
        """Retorna una conexión activa a la base de datos específica."""
        config = DB_CONFIG.copy()
        try:
            conn = mysql.connector.connect(**config)
            return conn
        except mysql.connector.Error as err:
            DBConnection.error=err
            raise err