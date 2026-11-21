"""Configuración centralizada del registro de eventos y errores."""
import logging  # módulo estándar de Python para registrar eventos y errores
from pathlib import Path  # Path permite construir rutas de archivo de forma segura


# Ruta del archivo de log: queda junto a este archivo, sin importar desde dónde se ejecute
RUTA_LOG = Path(__file__).resolve().parent / "software_fj.log"
logger = logging.getLogger("software_fj")  # crea (o recupera) el logger llamado software_fj
logger.setLevel(logging.INFO)  # registra mensajes desde el nivel INFO hacia arriba
logger.propagate = False  # evita que los mensajes se dupliquen en el logger raíz

# Agrega el manejador de archivo solo si todavía no existe uno para esta ruta (evita líneas duplicadas)
if not any(
    isinstance(handler, logging.FileHandler)  # el manejador existente es de tipo archivo
    and Path(handler.baseFilename).resolve() == RUTA_LOG.resolve()  # y escribe en este mismo archivo de log
    for handler in logger.handlers  # revisa los manejadores ya registrados
):
    handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # crea el manejador que escribe en el archivo, en UTF-8
    handler.setFormatter(  # define el formato de cada línea del log
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # fecha y hora | nivel (INFO/ERROR) | mensaje
    )
    logger.addHandler(handler)  # conecta el manejador al logger


# Registra un evento normal (operación correcta)
def registrar_evento(mensaje):
    """Guarda un evento normal del sistema."""
    logger.info(mensaje)  # escribe el mensaje con nivel INFO


# Registra un error con su tipo, mensaje y traza completa
def registrar_error(operacion, error):
    """Guarda el error, su tipo y la traza que permite localizarlo."""
    logger.error(  # escribe con nivel ERROR
        "%s | %s: %s",  # formato: operación | tipo de error: mensaje
        operacion,  # descripción de la operación que falló
        type(error).__name__,  # nombre de la clase de la excepción
        error,  # mensaje de la excepción
        exc_info=(type(error), error, error.__traceback__),  # incluye la traza (traceback) para ubicar dónde ocurrió el error
    )
