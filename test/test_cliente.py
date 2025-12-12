from datetime import date
import mysql.connector
import pytest
from unittest.mock import MagicMock

# Imports corregidos
from entidades.cliente import Cliente
from dao.conexion import DBConnection
from dao.clienteDAO import ClienteDAO
from servicios.servicio import ClienteService
# Importamos el controlador que acabamos de crear
from controladores.cevicheriaController import CevicheríaController

# =========================================================
# PRUEBAS UNITARIAS (Aislando la Capa de Servicio)
# =========================================================

def test_guardar_cliente_unitario_exitoso(mocker):
    """Prueba unitaria para registro exitoso."""
    # CORRECCIÓN: 'dao.clienteDAO.ClienteDAO' (clienteDAO en minúscula como el archivo)
    mock_dao_guardar = mocker.patch(
        'dao.clienteDAO.ClienteDAO.guardar',
        return_value=5
    )

    service = ClienteService()
    cliente_registrado = service.registrar_cliente("Test Mock", "123456789")

    mock_dao_guardar.assert_called_once()
    assert cliente_registrado is not None
    assert cliente_registrado.nombre == "Test Mock"
    assert isinstance(cliente_registrado, Cliente)


def test_guardar_cliente_unitario_fallido(mocker):
    """Prueba unitaria para fallo en registro."""
    # CORRECCIÓN: Ruta del mock corregida
    mock_dao_guardar = mocker.patch(
        'dao.clienteDAO.ClienteDAO.guardar',
        return_value=-1
    )

    service = ClienteService()
    cliente_registrado = service.registrar_cliente("Test Fallo", "111222333")

    mock_dao_guardar.assert_called_once()
    assert cliente_registrado is None


# =========================================================
# PRUEBAS DE INTEGRACIÓN
# =========================================================

def test_registro_cliente_integracion_fallo_db(mocker):
    """
    Prueba de integración: Simula fallo de conexión a la BD.
    """
    # 1. Crear el error simulado
    mock_error = mysql.connector.Error(msg="Simulated DB Connection Error")

    # 2. Mockear la conexión para que falle. 
    # CORRECCIÓN: Ruta 'dao.conexion.DBConnection' (conexion en minúscula)
    mock_conn = mocker.patch(
        'dao.conexion.DBConnection.get_connection',
        side_effect=mock_error
    )

    # 3. Inicializar el controlador (Ahora sí existe la clase)
    controller = CevicheríaController()
    items = [{'plato_id': 1, 'cantidad': 1}]
    fecha_actual = date.today()

    # 4. Ejecutar
    # Al llamar a este método, el controlador intentará usar el servicio,
    # el servicio intentará usar el DAO, y el DAO intentará conectar a la BD.
    # Ahí explotará el Mock, y el controlador deberá capturar el error.
    orden_fallida = controller.registrar_nueva_orden(
        cliente_id=1,
        tipo_orden='I',
        items=items,
        fecha=fecha_actual
    )

    # 5. Verificación
    # Verificamos que se intentó conectar (y falló)
    mock_conn.assert_called()
    
    # El controlador debe haber manejado la excepción y retornado None
    assert orden_fallida is None