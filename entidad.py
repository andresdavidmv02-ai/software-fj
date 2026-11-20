from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase abstracta común para las entidades de Software FJ."""

    def __init__(self, identificador):
        if identificador is None or not str(identificador).strip():
            raise ValueError("El identificador es obligatorio")

        self._identificador = str(identificador).strip()
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        return self._identificador

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def mostrar_informacion(self):
        """Devuelve una descripción legible de la entidad."""
        raise NotImplementedError
