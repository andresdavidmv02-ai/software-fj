"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSistemaFJ(Exception):
    """Excepción base del sistema."""
    # Todas las demás excepciones heredan de esta; así se capturan todas con un solo except.


class ClienteInvalidoError(ErrorSistemaFJ):
    """Datos del cliente inválidos o identificador duplicado."""


class ParametroInvalidoError(ErrorSistemaFJ):
    """Parámetro inválido o faltante al crear o usar un servicio."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """El servicio existe, pero no se puede reservar en este momento."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """La reserva no se pudo crear o procesar."""


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Operación no válida para el estado actual de una reserva."""


class CalculoInconsistenteError(ErrorSistemaFJ):
    """El cálculo de costos produjo un resultado cero, negativo o inválido."""
