import unittest
from datetime import date
from unittest.mock import MagicMock, patch
from dao.ordenDAO import OrdenDAO
from servicios.servicio import ClienteService

class TestFidelidad(unittest.TestCase):

    # --- 1. PRUEBA UNITARIA (DAO: Contar Órdenes) ---
    @patch('dao.conexion.DBConnection.get_connection')
    def test_dao_contar_ordenes_sql(self, mock_get_conn):
        """Valida que el DAO ejecute el SELECT COUNT correcto."""
        # Mockear BD
        mock_cursor = MagicMock()
        mock_get_conn.return_value.cursor.return_value = mock_cursor
        
        # Simulamos que la BD responde "(5)" (5 órdenes encontradas)
        mock_cursor.fetchone.return_value = (5,)

        # Ejecutar
        dao = OrdenDAO()
        cantidad = dao.contar_ordenes_ultimo_mes(1, date.today())

        # Verificar
        self.assertEqual(cantidad, 5)
        # Verificamos que el SQL tenga el COUNT y el filtro de fecha
        sql_arg = mock_cursor.execute.call_args[0][0]
        self.assertIn("SELECT COUNT(*)", sql_arg)
        self.assertIn("fecha >=", sql_arg)

    # --- 2. PRUEBA DE INTEGRACIÓN (Servicio: Lógica de Negocio) ---
    def test_servicio_fidelidad_aprobada(self):
        """Cliente con 4 órdenes DEBE tener fidelidad (True)."""
        service = ClienteService()
        
        # TRUCO: Inyectamos un Mock del OrdenDAO dentro del servicio
        # para no ir a la BD real, pero probar la lógica del IF/ELSE
        service.orden_dao = MagicMock()
        service.orden_dao.contar_ordenes_ultimo_mes.return_value = 4 # Tiene 4

        es_fiel = service.verificar_oferta_fidelidad(1)
        self.assertTrue(es_fiel, "Debería ser True si tiene 4 órdenes")

    def test_servicio_fidelidad_rechazada(self):
        """Cliente con 3 órdenes NO DEBE tener fidelidad (False)."""
        service = ClienteService()
        
        service.orden_dao = MagicMock()
        service.orden_dao.contar_ordenes_ultimo_mes.return_value = 3 # Tiene 3

        es_fiel = service.verificar_oferta_fidelidad(1)
        self.assertFalse(es_fiel, "Debería ser False si tiene 3 órdenes")

if __name__ == '__main__':
    unittest.main()