# 🐟 Sistema de Gestión Cevichería "Mar Adentro" (Lab 09)

Este proyecto implementa el backend para una cevichería utilizando una **Arquitectura en Capas** y la metodología **TDD (Test Driven Development)**.

Se hace uso intensivo de **Mocks** y **Pruebas de Integración** para validar la lógica de negocio sin depender de la base de datos MySQL real.

## 🏗️ Arquitectura del Software

El sistema sigue el patrón de separación de responsabilidades:

```text
SisRestaurante/
├── controladores/      # Orquestación y entrada de datos
│   ├── platoController.py
│   ├── ordenController.py
│   └── cevicheriaController.py
├── servicios/          # Lógica de Negocio (Reglas, Fidelidad)
│   ├── servicio.py     # ClienteService
│   ├── platoService.py
│   └── ordenService.py
├── dao/                # Acceso a Datos (SQL)
│   ├── conexion.py     # Singleton DB Connection
│   ├── clienteDAO.py
│   ├── platoDAO.py
│   └── ordenDAO.py
├── entidades/          # Modelos de Dominio
└── test/               # Pruebas Automatizadas (Pytest)
```

## 📋 Requisitos

*   **Python 3.x**
*   Librerías: `pytest`, `pytest-mock`, `mysql-connector-python`.

## 🧪 Ejecución de Pruebas

El proyecto cuenta con una cobertura de pruebas para los 3 módulos críticos.

### Ejecutar todas las pruebas (Recomendado)

```bash
python -m pytest test/
```