from entidad import Entidad


class Reserva(Entidad):
    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if cliente is None:
            raise ValueError("Debe seleccionar un cliente")

        if servicio is None:
            raise ValueError("Debe seleccionar un servicio")

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValueError("La duración debe ser mayor que cero")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != "Pendiente":
            raise ValueError("Solo se pueden confirmar reservas pendientes")

        self._estado = "Confirmada"

    def cancelar(self):
        if self._estado in ("Cancelada", "Procesada"):
            raise ValueError("No se puede cancelar esta reserva")

        self._estado = "Cancelada"

    def procesar(self):
        if self._estado != "Confirmada":
            raise ValueError("La reserva debe estar confirmada")

        try:
            costo = self._servicio.calcular_costo(self._duracion)

            if not isinstance(costo, (int, float)) or costo < 0:
                raise ValueError("El servicio devolvió un costo inválido")

        except Exception as error:
            raise RuntimeError(
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
            f"Duración: {self._duracion} | "
            f"Estado: {self._estado}"
        )
