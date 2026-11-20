"""Configuración centralizada del registro de eventos y errores."""
import logging
from pathlib import Path


RUTA_LOG = Path(__file__).resolve().parent / "software_fj.log"
logger = logging.getLogger("software_fj")
logger.setLevel(logging.INFO)
logger.propagate = False

if not any(
    isinstance(handler, logging.FileHandler)
    and Path(handler.baseFilename).resolve() == RUTA_LOG.resolve()
    for handler in logger.handlers
):
    handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(handler)


def registrar_evento(mensaje):
    """Guarda un evento normal del sistema."""
    logger.info(mensaje)


def registrar_error(operacion, error):
    """Guarda el error, su tipo y la traza que permite localizarlo."""
    logger.error(
        "%s | %s: %s",
        operacion,
        type(error).__name__,
        error,
        exc_info=(type(error), error, error.__traceback__),
    )
