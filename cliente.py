import re

from entidad import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):
    """Representa un cliente y valida sus datos personales."""

    def __init__(self, identificacion, nombre, correo, telefono):
        # Verifica que la identificación no esté vacía.
        if identificacion is None or not str(identificacion).strip():
            raise ClienteInvalidoError("La identificacion es obligatoria")

        # Inicializa el identificador heredado de la clase Entidad.
        super().__init__(str(identificacion).strip())

        # Asigna los datos utilizando propiedades para validar cada valor.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        """Devuelve el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Comprueba que el nombre sea texto y tenga al menos 3 caracteres.
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre debe tener al menos 3 caracteres"
            )

        self._nombre = valor.strip()

    @property
    def correo(self):
        """Devuelve el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor):
        # Verifica que el correo recibido sea una cadena de texto.
        if not isinstance(valor, str):
            raise ClienteInvalidoError("El correo debe ser texto")

        correo = valor.strip()

        # Expresión regular para comprobar el formato del correo electrónico.
        patron = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"

        if not re.fullmatch(patron, correo):
            raise ClienteInvalidoError(
                "El correo electronico no es valido"
            )

        self._correo = correo

    @property
    def telefono(self):
        """Devuelve el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        # Convierte el teléfono a texto y elimina espacios al inicio y al final.
        telefono = str(valor).strip()

        # Comprueba que solo tenga números y entre 7 y 15 dígitos.
        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise ClienteInvalidoError(
                "El telefono debe contener entre 7 y 15 digitos"
            )

        self._telefono = telefono

    def mostrar_informacion(self):
        """Devuelve los datos principales del cliente en un solo texto."""
        # Organiza la información para mostrarla de forma clara.
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )
