"""Prueba rápida de servicios.py (parte de servicios y excepciones).

Funciona aunque todavía no exista entidad.py del compañero: en ese caso
usa una clase Entidad temporal solo para poder probar.
Ejecutar:  python prueba_servicios.py
"""
import sys
import types
from abc import ABC, abstractmethod

try:
    import entidad  # intenta usar el archivo real del compañero
except ModuleNotFoundError:
    # Versión temporal con lo mínimo que necesita Servicio (copia de la idea de Entidad)
    class Entidad(ABC):
        def __init__(self, identificador):
            if not identificador:
                raise ValueError("El identificador es obligatorio")
            self._identificador = str(identificador)

        @property
        def identificador(self):
            return self._identificador

        @abstractmethod
        def mostrar_informacion(self):
            """Cada entidad muestra su información."""

    temporal = types.ModuleType("entidad")  # módulo falso en memoria
    temporal.Entidad = Entidad
    sys.modules["entidad"] = temporal  # así 'from entidad import Entidad' funciona

from excepciones import ErrorSistemaFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio


def probar(titulo, funcion):
    """Ejecuta una prueba y muestra si salió bien o si se lanzó una excepción controlada."""
    try:
        resultado = funcion()
        print(f"OK   - {titulo}: {resultado}")
    except (ErrorSistemaFJ, TypeError) as error:
        print(f"ERR  - {titulo}: {type(error).__name__}: {error}")


# 1. No se puede instanciar la clase abstracta
probar("Instanciar Servicio abstracta", lambda: Servicio("x", 100))

# 2. Servicios válidos y su información (polimorfismo)
sala = ReservaSala("Sala Norte", 50000, 10)
equipo = AlquilerEquipo("Portátil", 15000, seguro=5000)
asesoria = AsesoriaEspecializada("Consultoría Python", 80000, "senior")
for servicio in (sala, equipo, asesoria):
    print("Info:", servicio.mostrar_informacion())

# 3. Costos con parámetros opcionales (la 'sobrecarga')
probar("Sala 3h sin impuesto", lambda: sala.calcular_costo(3))
probar("Sala 3h con IVA 19%", lambda: sala.calcular_costo(3, 0.19))
probar("Equipo 2h con IVA y 10% desc.", lambda: equipo.calcular_costo(2, 0.19, 0.10))
probar("Asesoría senior 2h", lambda: asesoria.calcular_costo(2))

# 4. Casos inválidos (deben lanzar excepciones controladas)
probar("Sala con capacidad 0", lambda: ReservaSala("Sala X", 50000, 0))
probar("Equipo con tarifa negativa", lambda: AlquilerEquipo("Proyector", -100))
probar("Asesoría con nivel inventado", lambda: AsesoriaEspecializada("Ase", 80000, "experto"))
probar("Asesoría sin parámetros", lambda: AsesoriaEspecializada())
probar("Impuesto fuera de rango", lambda: sala.calcular_costo(2, 5))
