
from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    def __init__(self, identificador):
        if not identificador:
            raise ValueError("El identificador es obligatorio")

        self._identificador = str(identificador)
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        return self._identificador

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def mostrar_informacion(self):
        pass
