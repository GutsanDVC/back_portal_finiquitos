# Este archivo convierte a 'utils' en un paquete Python importable.
# Puedes exponer utilidades comunes aquí si lo deseas.
from .txt_logger import writeTxtLog, DEFAULT_LOG_DIR, DEFAULT_LOG_FILE

__all__ = [
    "writeTxtLog",
    "DEFAULT_LOG_DIR",
    "DEFAULT_LOG_FILE",
]
