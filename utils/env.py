# utils/env.py

import os
from dotenv import load_dotenv

def load_env(path: str = ".env") -> None:
    """
    Carga las variables de entorno desde un archivo .env.

    Args:
        path (str): Ruta al archivo .env (por defecto ".env").
    """
    loaded = load_dotenv(dotenv_path=path)
    if not loaded:
        raise FileNotFoundError(f"No se pudo cargar el archivo {path}")
    else:
        print(f".env cargado desde {path}")

def get_env_var(key: str, default=None):
    """
    Obtiene una variable de entorno con un valor por defecto.

    Args:
        key (str): Nombre de la variable de entorno.
        default: Valor a devolver si la variable no existe.

    Returns:
        str | None: Valor de la variable o el valor por defecto.
    """
    return os.getenv(key, default)
