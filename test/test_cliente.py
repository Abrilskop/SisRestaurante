# test_cliente.py
from datetime import date

import mysql.connector
import pytest
from unittest.mock import MagicMock
from entidades.cliente import Cliente
from dao.conexion import DBConnection
from dao.clienteDAO import  ClienteDAO  # Asumimos que DBConnection y ClienteDAO están disponibles
from servicios.servicio import ClienteService

# =========================================================
# PRUEBAS UNITARIAS (Aislando la Capa de Servicio)
# =========================================================

# Usamos la fixture 'mocker' proporcionada por pytest-mock
def test_guardar_cliente_unitario_exitoso(mocker):
    """
    Prueba unitaria para ClienteService.registrar_cliente().
    Aísla la capa de servicio 'mockeando' la capa DAO.
    """

    # 1. Preparación del Mock: Simular que ClienteDAO.guardar() retorna un ID (éxito)
    # Creamos un mock para el método guardar del DAO.
    mock_dao_guardar = mocker.patch(
        'dao.ClienteDAO.guardar',
        return_value=5
    )

    # 2. Inicialización del servicio
    service = ClienteService()

    # 3. Ejecución
    # No necesitamos pasar una instancia de Cliente real, solo los datos.
    cliente_registrado = service.registrar_cliente("Test Mock", "123456789")

    # 4. Verificación (Asserts)

    # Aseguramos que el método 'guardar' del DAO fue llamado exactamente una vez
    mock_dao_guardar.assert_called_once()

    # Aseguramos que la función de servicio retorna un objeto Cliente válido
    assert cliente_registrado is not None
    assert cliente_registrado.nombre == "Test Mock"
    # El servicio no debe asignar el ID devuelto por el DAO a menos que se implemente buscar_por_id,
    # pero aquí validamos que retorna un objeto:
    assert isinstance(cliente_registrado, Cliente)


def test_guardar_cliente_unitario_fallido(mocker):
    """
    Prueba unitaria para ClienteService.registrar_cliente().
    Simula que el DAO falla al guardar (ej. teléfono duplicado).
    """

    # 1. Preparación del Mock: Simular que ClienteDAO.guardar() retorna -1 (fallo)
    mock_dao_guardar = mocker.patch(
        'dao.ClienteDAO.guardar',
        return_value=-1
    )

    # 2. Inicialización del servicio
    service = ClienteService()

    # 3. Ejecución
    cliente_registrado = service.registrar_cliente("Test Fallo", "111222333")

    # 4. Verificación (Asserts)

    # Aseguramos que el método 'guardar' del DAO fue llamado
    mock_dao_guardar.assert_called_once()

    # El servicio debe retornar None si el DAO falló
    assert cliente_registrado is None


# =========================================================
# PRUEBAS DE INTEGRACIÓN (Controller, Service, DAO, DBConnection)
# =========================================================

# Nota: Esta prueba NO USA MOCKS para el DAO ni la BD,
# sino que usa un Mock para la función crítica DBConnection.get_connection()
# y simula una excepción en la base de datos para verificar el manejo de errores.

def test_registro_cliente_integracion_fallo_db(mocker):
    """
    Prueba de integración para CevicheríaController.registrar_nueva_orden().
    Simula un fallo total de conexión a la BD para verificar que el flujo del
    Controlador y el Servicio manejen la excepción correctamente.
    """

    # 1. Preparación del Mock: Simular un fallo de conexión en la capa más baja

    # Creamos un objeto de excepción de MySQL simulado.
    mock_error = mysql.connector.Error(msg="Simulated DB Connection Error")


    mock_conn = mocker.patch(
        'dao.DBConnection.get_connection',
        side_effect=mock_error
    )

    controller = CevicheríaController()
    items = [{'plato_id': 1, 'cantidad': 1}]
    fecha_actual = date.today()

    # El método 'registrar_nueva_orden' llama a 'crear_orden' que, a su vez,
    # llama al DAO para buscar el cliente (que fallará la conexión).

    # Este test verifica que el método del controlador maneje el error y retorne None/Fallo.
    orden_fallida = controller.registrar_nueva_orden(
        cliente_id=1,
        tipo_orden='I',
        items=items,
        fecha=fecha_actual
    )

    # 4. Verificación (Asserts)

    # El método de conexión debe haber sido llamado
    mock_conn.assert_called()

    # El controlador debe retornar None (o un valor indicando fallo) cuando la conexión falla
    assert orden_fallida is None