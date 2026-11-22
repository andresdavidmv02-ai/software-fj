# Software FJ: gestión de clientes, servicios y reservas

Proyecto de programación orientada a objetos en Python, sin base de datos.
Curso Programación (213023) – Universidad Nacional Abierta y a Distancia (UNAD), Fase 4.

## Integrantes

- Andrés David Muñoz Vargas
- Ever Steven Salinas Reyes

## ¿Qué hace?

Gestiona clientes, servicios (reserva de salas, alquiler de equipos y asesorías especializadas) y reservas de la empresa Software FJ. Valida los datos con rigor y maneja los errores sin detener el programa: cada error o evento se registra en un archivo de log.

## Conceptos aplicados

- **Abstracción:** clases abstractas `Entidad` y `Servicio`.
- **Herencia y polimorfismo:** `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` sobrescriben `calcular_costo()` y `describir()`.
- **Encapsulación:** atributos protegidos con propiedades y validaciones (`Cliente`, `Reserva`).
- **Sobrecarga simulada:** `calcular_costo(horas, impuesto=0.0, descuento=0.0)` con parámetros opcionales.
- **Manejo de excepciones:** excepciones personalizadas, `try/except/else/finally` y encadenamiento con `raise ... from`.
- **Registro de eventos:** todos los errores y eventos relevantes se guardan en `software_fj.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| `entidad.py` | Clase abstracta general `Entidad` |
| `cliente.py` | Clase `Cliente` con validaciones |
| `servicios.py` | Clase abstracta `Servicio` y tres servicios especializados |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar y procesar) |
| `excepciones.py` | Excepciones personalizadas del sistema |
| `logs.py` | Configuración del archivo de log |
| `main.py` | Simulación de 17 operaciones, válidas e inválidas |
| `prueba_servicios.py` | Pruebas de los servicios y sus validaciones |
| `prueba_integracion.py` | Pruebas de integración entre clases |

## Cómo ejecutarlo

Requisitos: Python 3.9 o superior. No usa librerías externas.

```
python main.py
python prueba_servicios.py
python prueba_integracion.py
```

`main.py` ejecuta 17 operaciones (10 exitosas y 7 con error controlado) y deja el registro en `software_fj.log`. Las pruebas deben terminar sin fallos.
