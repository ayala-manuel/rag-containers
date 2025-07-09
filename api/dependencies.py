# api/dependencies.py

from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette import HTTP_401_UNAUTHORIZED
from utils.env import get_env_var, load_dotenv

load_dotenv()

API_KEY = get_env_var("API_KEY")

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)) -> None:
    """Verifica la clave API proporcionada en el encabezado de la solicitud.

    Args:
        api_key (str): Clave API proporcionada en el encabezado de la solicitud.

    Raises:
        HTTPException: Si la clave API no es válida.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
            )