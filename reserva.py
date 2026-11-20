import math

from cliente import Cliente
from entidad import Entidad
from excepciones import (
    CalculoInconsistenteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from servicios import Servicio


class Reserva(Entidad):
    """Relaciona un cliente con un servicio y controla el estado de la reserva."""

    ESTADOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, identificador, cliente, servicio, duracion):
        try:
            super().__init__(identificador)
        except ValueError as error:
            raise ReservaInvalidaError(str(error)) from error

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "Debe seleccionar un cliente válido"
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "Debe seleccionar un servicio válido"
            )

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise ReservaInvalidaError(
                "La duración debe ser un número mayor que cero"
            )

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio seleccionado no está disponible"
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    def confirmar(self):
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes"
            )

        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio dejó de estar disponible"
            )

        self._estado = "Confirmada"

        return f"Reserva {self.identificador} confirmada correctamente."

    def cancelar(self):
        if self._estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva cancelada o procesada"
            )

        self._estado = "Cancelada"

        return f"Reserva {self.identificador} cancelada correctamente."

    def procesar(self):
        if self._estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada para procesarse"
            )

        try:
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    "El servicio no está disponible"
                )

            costo = self._servicio.calcular_costo(self._duracion)

            if (
                isinstance(costo, bool)
                or not isinstance(costo, (int, float))
                or not math.isfinite(costo)
                or costo <= 0
            ):
                raise CalculoInconsistenteError(
                    "El servicio devolvió un costo inválido"
                )

        except Exception as error:
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva"
            ) from error

        else:
            self._estado = "Procesada"
            return costo

        finally:
            print(
                f"Finalizando intento de procesamiento: "
                f"{self.identificador}"
            )

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.descripcion} | "
            f"Duración: {self._duracion} h | "
            f"Estado: {self._estado}"
        )
