# utils/ids.py

import uuid

def generate_uuid4() -> str:
    """
    Genera un UUID versión 4 como string.
    """
    return str(uuid.uuid4())

def generate_custom_id(prefix: str = "") -> str:
    """
    Genera un UUID versión 4 con un prefijo opcional.
    
    Args:
        prefix (str): Texto que se antepone al UUID.

    Returns:
        str: Prefijo + UUID4.
    """
    return f"{prefix}{uuid.uuid4()}"
