import unittest
from datetime import date
from unittest.mock import MagicMock, patch
from entidades.orden import Orden
# Estos imports fallarán ahora (Fase Roja)
from dao.ordenDAO import OrdenDAO
from controladores.ordenController import OrdenController
from servicios.ordenService import OrdenService

class TestOrden(unittest.TestCase):

    # --- 1. PRUEBA UNITARIA (DAO) ---
    @patch('dao.conexion.DBConnection.get_connection')
    def test_guardar_orden_unitario(self, mock_get_conn):
        """Valida que el DAO inserte la orden correctamente."""
        # Preparar Mock BD
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 100  # ID simulado

        # Ejecutar
        dao = OrdenDAO()
        # Orden: cliente 1, fecha hoy, tipo Individual, total 50.0
        orden = Orden(1, date.today(), 'I', 50.0)
        id_res = dao.guardar(orden)

        # Verificar
        self.assertEqual(id_res, 100)
        mock_cursor.execute.assert_called_once()
        # Verificar SQL
        args, _ = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO orden", args[0])

    # --- 2. PRUEBA DE INTEGRACIÓN (Controlador -> Servicio) ---
    @patch('dao.ordenDAO.OrdenDAO.guardar')
    def test_integracion_controlador_orden(self, mock_dao_guardar):
        """Valida el flujo completo Controlador -> Servicio -> DAO"""
        # Simular éxito del DAO (ID 101)
        mock_dao_guardar.return_value = 101

        # Inicializar
        ctrl = OrdenController()
        
        # Ejecutar
        # Cliente 1, Tipo Familiar, Total 120.0
        resultado = ctrl.crear_orden(1, 'F', 120.0)

        # Verificar
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 101) # Valida que el servicio asigne el ID
        self.assertEqual(resultado.cliente_id, 1)
        self.assertEqual(resultado.tipo_orden, 'F')

if __name__ == '__main__':
    unittest.main()