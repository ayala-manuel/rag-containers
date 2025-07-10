
# Mercados Qdrant API

API REST para la gestión y búsqueda de documentos en colecciones vectoriales utilizando **Qdrant** como motor de búsqueda semántica.

---

## 🗂 Estructura del proyecto

```
.
├── api/
│   ├── Dockerfile
│   ├── main.py            # Entrada principal de la API
│   ├── routes.py          # Definición de rutas y endpoints
│   ├── schemas.py         # Modelos Pydantic para validación
│   ├── dependencies.py    # Dependencias comunes para FastAPI
│   └── requirements.txt   # Dependencias específicas API
├── core/
│   └── client.py          # Cliente de conexión a Qdrant
├── embeddings_service/
│   ├── Dockerfile
│   ├── main.py            # Servicio para generar embeddings
│   ├── schemas.py         # Modelos Pydantic específicos embeddings
│   └── requirements.txt
├── utils/
│   ├── chunking.py
│   ├── embedding_client.py
│   ├── env.py
│   ├── ids.py
│   ├── payload.py
│   ├── query_filters.py   # Lógica de filtros para búsquedas
│   ├── serialization.py
│   └── utils.py
├── docker-compose.yml     # Orquestador de servicios Docker
├── poetry.lock
├── pyproject.toml
└── resources/             # Recursos estáticos
```

---

## Funcionalidades principales

- Crear, listar y eliminar colecciones en Qdrant.
- Subir documentos enriquecidos con metadata (fecha, tags, imágenes).
- Realizar búsquedas vectoriales filtradas por metadata.
- Servicio dedicado para generación de embeddings de texto.
- Configurado para ejecutarse con Docker y Docker Compose.

---

## API Endpoints destacados

- **GET** `/api/`  
  Mensaje de bienvenida.

- **GET** `/api/ping`  
  Verifica disponibilidad de la API.

- **GET** `/api/collections`  
  Lista todas las colecciones (requiere API Key).

- **POST** `/api/collections/create`  
  Crea una nueva colección (requiere API Key).

- **DELETE** `/api/collections/{collection_name}`  
  Elimina una colección (requiere API Key).

- **POST** `/api/collections/{collection_name}/upload`  
  Subir documentos a la colección.

- **POST** `/api/collections/{collection_name}/search`  
  Buscar documentos con query y filtros.

- **POST** `/api/embed`  
  Obtener embeddings para textos.

---

## Autenticación

Para los endpoints que la requieren, añade en el header HTTP:

```
Authorization: "contraseña"
```

---

## Ejemplo de subida de documentos

```json
[
  {
    "text": "Contenido del documento",
    "metadata": {
      "title": "Ejemplo de documento",
      "date": "2025-07-10",
      "tags": ["ejemplo", "test"],
      "images": ["url_imagen_1", "url_imagen_2"] -> EN DESARROLLO
    }
  }
]
```

---

## Levantar el proyecto con Docker Compose

```bash
docker-compose up --build
```

Esto levantará la API y el servicio de embeddings configurados.

---

## Requisitos para desarrollo local

- Python 3.10+
- Poetry para manejo de dependencias (opcional)
- Instalar dependencias:

```bash
cd api
pip install -r requirements.txt

cd ../embeddings_service
pip install -r requirements.txt
```
