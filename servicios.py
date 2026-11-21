"""Clase abstracta Servicio y tres servicios especializados."""
import math  # se usa math.isfinite para rechazar valores como inf o nan
from abc import abstractmethod  # permite declarar métodos abstractos

from entidad import Entidad  # clase general abstracta (parte del compañero)
from excepciones import CalculoInconsistenteError, ParametroInvalidoError  # excepciones propias


class Servicio(Entidad):
    """Servicio genérico; sus clases hijas calculan costos polimórficamente."""

    _contador = 0  # contador compartido por todos los servicios para generar su identificador

    def __init__(self, nombre, tarifa_hora, disponible=True):
        self._nombre = nombre  # nombre del servicio
        self._tarifa_hora = tarifa_hora  # valor que se cobra por cada hora
        self._disponible = disponible  # True si el servicio se puede reservar
        self.validar_parametros()  # valida ANTES de crear el id; si falla, no se gasta un número
        Servicio._contador += 1  # incrementa el contador solo cuando los datos son válidos
        super().__init__(f"SRV-{Servicio._contador:03d}")  # id tipo SRV-001 para la clase Entidad

    @property
    def nombre(self):
        return self._nombre  # solo lectura: no hay setter, así no se cambia desde fuera

    @property
    def disponible(self):
        return self._disponible  # indica si se puede reservar ahora

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):  # solo se acepta True o False
            raise ParametroInvalidoError("La disponibilidad debe ser True o False")
        self._disponible = valor  # activa o desactiva el servicio

    @property
    def descripcion(self):
        return self.describir()  # atajo que usa Reserva.mostrar_informacion

    def validar_parametros(self):
        # El nombre debe ser texto y no estar vacío
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ParametroInvalidoError("El nombre del servicio es obligatorio")
        # La tarifa debe ser un número finito mayor que cero (y no un bool, que en Python es int)
        if (isinstance(self._tarifa_hora, bool)
                or not isinstance(self._tarifa_hora, (int, float))
                or not math.isfinite(self._tarifa_hora)
                or self._tarifa_hora <= 0):
            raise ParametroInvalidoError("La tarifa por hora debe ser mayor que cero")
        # La disponibilidad debe ser estrictamente True o False
        if not isinstance(self._disponible, bool):
            raise ParametroInvalidoError("La disponibilidad debe ser True o False")

    def _validar_calculo(self, horas, impuesto, descuento):
        # Las horas deben ser un número finito mayor que cero
        if (isinstance(horas, bool) or not isinstance(horas, (int, float))
                or not math.isfinite(horas) or horas <= 0):
            raise ParametroInvalidoError("Las horas deben ser un número mayor que cero")
        # Impuesto y descuento son proporciones: 0.19 = 19 %, deben estar entre 0 y 1
        for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if (isinstance(valor, bool) or not isinstance(valor, (int, float))
                    or not math.isfinite(valor) or not 0 <= valor <= 1):
                raise ParametroInvalidoError(f"El {nombre} debe estar entre 0 y 1")

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """Calcula el costo; parámetros opcionales simulan sobrecarga."""
        # Los parámetros opcionales permiten llamar: calcular_costo(2), (2, 0.19) o (2, 0.19, 0.1)
        raise NotImplementedError  # cada clase hija debe sobrescribir este método

    @abstractmethod
    def describir(self):
        """Devuelve la descripción específica del servicio."""
        raise NotImplementedError  # cada clase hija debe sobrescribir este método

    def mostrar_informacion(self):
        # Implementa el método abstracto de Entidad: id + descripción del servicio
        return f"{self.identificador} | {self.describir()}"

    def _aplicar(self, base, impuesto, descuento):
        # Aplica impuesto (suma) y descuento (resta) sobre el valor base y redondea a 2 decimales
        costo = round(base * (1 + impuesto) * (1 - descuento), 2)
        if not math.isfinite(costo) or costo <= 0:  # un costo cero o negativo es inconsistente
            raise CalculoInconsistenteError(
                "El cálculo produjo un costo cero o negativo"
            )
        return costo


class ReservaSala(Servicio):
    """Servicio de reserva de salas con control de capacidad."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        self._capacidad = capacidad  # se asigna antes de llamar al padre, que valida todo
        super().__init__(nombre, tarifa_hora, disponible)  # inicializa los datos comunes

    def validar_parametros(self):
        super().validar_parametros()  # primero las validaciones comunes del padre
        # La capacidad debe ser un entero positivo (y no un bool)
        if (isinstance(self._capacidad, bool)
                or not isinstance(self._capacidad, int)
                or self._capacidad < 1):
            raise ParametroInvalidoError("La capacidad de la sala debe ser un entero positivo")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_calculo(horas, impuesto, descuento)  # valida horas, impuesto y descuento
        return self._aplicar(self._tarifa_hora * horas, impuesto, descuento)  # tarifa x horas

    def describir(self):
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) a ${self._tarifa_hora}/h"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos con cargo fijo de seguro."""

    def __init__(self, nombre, tarifa_hora, seguro=0, disponible=True):
        self._seguro = seguro  # cargo fijo por el seguro del equipo
        super().__init__(nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        super().validar_parametros()  # validaciones comunes
        # El seguro debe ser un número finito, no negativo (puede ser 0)
        if (isinstance(self._seguro, bool) or not isinstance(self._seguro, (int, float))
                or not math.isfinite(self._seguro) or self._seguro < 0):
            raise ParametroInvalidoError("El seguro no puede ser negativo")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_calculo(horas, impuesto, descuento)
        base = self._tarifa_hora * horas + self._seguro  # tarifa x horas + seguro fijo
        return self._aplicar(base, impuesto, descuento)

    def describir(self):
        return f"Equipo '{self._nombre}' a ${self._tarifa_hora}/h + seguro ${self._seguro}"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría con recargo según el nivel profesional."""

    RECARGOS = {"junior": 0.0, "senior": 0.25}  # recargo sobre la tarifa según el nivel

    def __init__(self, nombre=None, tarifa_hora=None, nivel="junior", disponible=True):
        # Normaliza el nivel a minúsculas y sin espacios si es texto
        self._nivel = nivel.lower().strip() if isinstance(nivel, str) else nivel
        # nombre y tarifa_hora = None permiten que falten y se rechacen con una excepción propia
        super().__init__(nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        super().validar_parametros()  # validaciones comunes (nombre y tarifa)
        if self._nivel not in self.RECARGOS:  # solo se aceptan los niveles definidos
            raise ParametroInvalidoError("El nivel debe ser 'junior' o 'senior'")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_calculo(horas, impuesto, descuento)
        base = self._tarifa_hora * horas * (1 + self.RECARGOS[self._nivel])  # aplica el recargo
        return self._aplicar(base, impuesto, descuento)

    def describir(self):
        return f"Asesoría '{self._nombre}' nivel {self._nivel} a ${self._tarifa_hora}/h"
