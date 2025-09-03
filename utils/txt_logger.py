from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
import sys

# -------------------------------------------------------------
# Utilidad simple para escribir logs en archivo .txt
# - Código en inglés, comentarios en español (según reglas globales)
# - Pensado para ser llamado desde cualquier módulo del proyecto
# -------------------------------------------------------------

DEFAULT_LOG_DIR = Path("logs")
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "app-log.txt"


def writeTxtLog(message: str, level: str, extra: Optional[Any] = None, filePath: Optional[str | Path] = None) -> bool:
    """Escribe una línea de log en un archivo .txt.

    Parámetros
    - message: Mensaje principal del log
    - level: Nivel del mensaje (ej: "INFO", "WARNING", "ERROR", "DEBUG")
    - extra: (opcional) Cualquier objeto a imprimir (se usará su repr())
    - filePath: (opcional) Ruta personalizada del archivo de log

    Retorna
    - bool: True si se escribió el log exitosamente, False en caso de error
    """
    try:
        # Normalizar ruta de archivo; por defecto en ./logs/app-log.txt
        log_path = Path(filePath) if filePath else DEFAULT_LOG_FILE
        log_path.parent.mkdir(parents=True, exist_ok=True)  # Crear carpeta si no existe

        # Timestamp ISO 8601 con zona horaria UTC para consistencia
        now = datetime.now(timezone.utc).isoformat()

        # Normalizar nivel en mayúsculas por consistencia visual
        level_str = str(level).upper() if level else "INFO"

        # Construir línea del log
        parts = [f"{now}", f"[{level_str}]", str(message)]
        if extra is not None:
            # Usamos repr() para preservar estructura útil en depuración
            parts.append(f"extra={repr(extra)}")
        line = " | ".join(parts)

        # Escribir en modo append con UTF-8
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

        return True
    except Exception as exc:
        # En caso de error, escribir aviso a stderr para no romper flujo de la app
        try:
            sys.stderr.write(f"writeTxtLog error: {exc}\n")
        except Exception:
            pass
        return False
