import unittest
from unittest.mock import MagicMock, patch
from entidades.plato import Plato
from dao.platoDAO import PlatoDAO
# Importamos el controlador y servicio que VAMOS a crear/modificar
# Si te sale error de import aquí, es normal en Fase Roja
from controladores.platoController import PlatoController
from servicios.platoService import PlatoService

class TestPlato(unittest.TestCase):

    # --- 1. PRUEBA UNITARIA (Guardar Plato en DAO) ---
    @patch('dao.conexion.DBConnection.get_connection')
    def test_guardar_plato_unitario(self, mock_get_conn):
        """Valida que el DAO construya bien el SQL y retorne el ID."""
        # Preparar Mock de la BD
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simulamos que la BD auto-genera el ID 10
        mock_cursor.lastrowid = 10 

        # Ejecutar
        dao = PlatoDAO()
        plato = Plato("Ceviche Test", "Picante", 35.0)
        id_generado = dao.guardar(plato)

        # Verificar
        self.assertEqual(id_generado, 10)
        self.assertEqual(plato.id, 10)
        # Verificar que se llamó al INSERT correcto
        mock_cursor.execute.assert_called_once()
        args, _ = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO plato", args[0])

    # --- 2. PRUEBA DE INTEGRACIÓN (Controlador -> Servicio) ---
    # Mockeamos el DAO para no tocar la BD, pero probamos el flujo del Controlador
    @patch('dao.platoDAO.PlatoDAO.guardar')
    def test_integracion_controlador_plato(self, mock_dao_guardar):
        """Valida que el Controlador llame al Servicio y este al DAO."""
        # Simulamos que el DAO responde éxito (ID 20)
        mock_dao_guardar.return_value = 20
        
        # Inicializar Controlador
        controlador = PlatoController()
        
        # Ejecutar acción del controlador
        resultado = controlador.crear_plato("Jalea Mixta", "Crujiente", 40.0)
        
        # Verificar
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 20)
        self.assertEqual(resultado.nombre, "Jalea Mixta")
        
        # Verificar que el DAO fue llamado al final de la cadena
        mock_dao_guardar.assert_called_once()

if __name__ == '__main__':
    unittest.main()