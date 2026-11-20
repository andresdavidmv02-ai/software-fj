from entidad import Entidad
from excepciones import ClienteInvalidoError
import re


class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo, telefono):
        if identificacion is None or not str(identificacion).strip():
            raise ClienteInvalidoError("La identificacion es obligatoria")

        super().__init__(str(identificacion).strip())

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre debe tener al menos 3 caracteres"
            )

        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise ClienteInvalidoError("El correo debe ser texto")

        correo = valor.strip()

        patron = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"

        if not re.fullmatch(patron, correo):
            raise ClienteInvalidoError(
                "El correo electronico no es valido"
            )

        self._correo = correo

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        telefono = str(valor).strip()

        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise ClienteInvalidoError(
                "El telefono debe contener entre 7 y 15 digitos"
            )

        self._telefono = telefono

    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )
