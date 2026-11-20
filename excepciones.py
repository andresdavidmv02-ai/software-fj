"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSistemaFJ(Exception):
    """Excepción base: todas las demás heredan de ella."""


class ClienteInvalidoError(ErrorSistemaFJ):
    """Datos del cliente inválidos (nombre, documento, correo...)."""


class ParametroInvalidoError(ErrorSistemaFJ):
    """Parámetro inválido o faltante al crear/usar un servicio."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """El servicio existe pero no se puede reservar ahora."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """La reserva no se pudo crear o procesar."""


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Operación no válida para el estado actual (ej. cancelar dos veces)."""


class CalculoInconsistenteError(ErrorSistemaFJ):
    """El cálculo de costos dio un resultado imposible (negativo o cero)."""
