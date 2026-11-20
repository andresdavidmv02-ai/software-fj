from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import ParametroInvalidoError


class Entidad(ABC):
    """Clase abstracta que representa las entidades generales del sistema."""

    def __init__(self, identificador):
        if identificador is None:
            raise ParametroInvalidoError(
                "El identificador es obligatorio"
            )

        identificador = str(identificador).strip()

        if not identificador:
            raise ParametroInvalidoError(
                "El identificador no puede estar vacio"
            )

        self._identificador = identificador
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        return self._identificador

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def mostrar_informacion(self):
        """Metodo que cada clase derivada debe implementar."""
        pass
