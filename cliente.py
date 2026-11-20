from entidad import Entidad
import re


class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.match(
            r"^[\w.+-]+@[\w-]+\.[\w.-]+$", valor
        ):
            raise ValueError("El correo electrónico no es válido")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        telefono = str(valor).strip()

        if not telefono.isdigit() or len(telefono) < 7:
            raise ValueError("El teléfono no es válido")

        self._telefono = telefono

    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )
