"""Clase abstracta Servicio y tres servicios especializados.

Hereda de Entidad (entidad.py, parte del compañero).
"""
from abc import abstractmethod  # para declarar métodos abstractos

from entidad import Entidad  # clase general creada por el compañero
from excepciones import ParametroInvalidoError  # excepción propia de este módulo


class Servicio(Entidad):
    """Servicio genérico de Software FJ (clase abstracta)."""

    _contador = 0  # cuenta los servicios creados para generar su identificador

    def __init__(self, nombre, tarifa_hora, disponible=True):
        self._nombre = nombre  # nombre del servicio
        self._tarifa_hora = tarifa_hora  # costo por hora
        self._disponible = disponible  # True si se puede reservar
        self.validar_parametros()  # valida ANTES de generar el id (así un servicio inválido no gasta número)
        Servicio._contador += 1  # incrementa el contador compartido
        super().__init__(f"SRV-{Servicio._contador:03d}")  # id tipo SRV-001 para la clase Entidad

    @property
    def nombre(self):
        """Nombre del servicio (solo lectura)."""
        return self._nombre

    @property
    def disponible(self):
        """Indica si el servicio se puede reservar."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)  # activa o desactiva el servicio

    @property
    def descripcion(self):
        """Texto descriptivo; lo usa la clase Reserva del compañero."""
        return self.describir()

    def validar_parametros(self):
        """Validación común; las clases hijas la amplían con super()."""
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ParametroInvalidoError("El nombre del servicio es obligatorio")
        if not isinstance(self._tarifa_hora, (int, float)) or self._tarifa_hora <= 0:
            raise ParametroInvalidoError(f"Tarifa inválida: {self._tarifa_hora!r}")

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """Costo total. Los parámetros opcionales simulan la sobrecarga en Python:
        calcular_costo(2) / calcular_costo(2, 0.19) / calcular_costo(2, 0.19, 0.1)."""

    @abstractmethod
    def describir(self):
        """Cada servicio se describe a sí mismo (polimorfismo)."""

    def mostrar_informacion(self):
        """Implementa el método abstracto de Entidad."""
        return f"{self.identificador} | {self.describir()}"

    def _aplicar(self, base, impuesto, descuento):
        """Aplica impuesto y descuento sobre un valor base (uso interno)."""
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ParametroInvalidoError("Impuesto y descuento deben estar entre 0 y 1")
        return round(base * (1 + impuesto) * (1 - descuento), 2)


class ReservaSala(Servicio):
    """Reserva de salas, con capacidad máxima de personas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        self._capacidad = capacidad  # se asigna antes de validar en la clase padre
        super().__init__(nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        super().validar_parametros()  # primero las validaciones comunes
        if not isinstance(self._capacidad, int) or self._capacidad < 1:
            raise ParametroInvalidoError(f"Capacidad inválida: {self._capacidad!r}")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        base = self._tarifa_hora * horas  # costo base = tarifa x horas
        return self._aplicar(base, impuesto, descuento)

    def describir(self):
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) a ${self._tarifa_hora}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos, con un cargo fijo de seguro."""

    def __init__(self, nombre, tarifa_hora, seguro=0, disponible=True):
        self._seguro = seguro  # cargo fijo por el seguro del equipo
        super().__init__(nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        super().validar_parametros()
        if not isinstance(self._seguro, (int, float)) or self._seguro < 0:
            raise ParametroInvalidoError(f"Seguro inválido: {self._seguro!r}")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        base = self._tarifa_hora * horas + self._seguro  # suma el seguro fijo
        return self._aplicar(base, impuesto, descuento)

    def describir(self):
        return f"Equipo '{self._nombre}' a ${self._tarifa_hora}/h + seguro ${self._seguro}"


class AsesoriaEspecializada(Servicio):
    """Asesoría con recargo según el nivel del asesor."""

    RECARGOS = {"junior": 0.0, "senior": 0.25}  # recargo por nivel

    def __init__(self, nombre, tarifa_hora, nivel="junior", disponible=True):
        self._nivel = nivel
        super().__init__(nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        super().validar_parametros()
        if self._nivel not in self.RECARGOS:
            raise ParametroInvalidoError(f"Nivel inválido: {self._nivel!r}")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        base = self._tarifa_hora * horas * (1 + self.RECARGOS[self._nivel])  # aplica recargo por nivel
        return self._aplicar(base, impuesto, descuento)

    def describir(self):
        return f"Asesoría '{self._nombre}' nivel {self._nivel} a ${self._tarifa_hora}/h"
