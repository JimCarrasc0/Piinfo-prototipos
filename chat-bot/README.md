<pre>
      ⌨️  ⌨️  ⌨️
        ┌───────────────┐
        │  CTRL ALT DEL │
        └───────────────┘

              /^-----^\
             V  o o  V
              |  Y  |
               \ Q /
               / - \
               |    \
               |     \     )
               || (___\====

</pre>

# T-Radar – BandurrIA Chatbot Backend

Backend del asistente BandurrIA, componente del proyecto T-Radar.  
Este servicio expone una API REST que integra detección de intención, capa semántica, recuperación de contexto (RAG) y un modelo de lenguaje para análisis de publicaciones en redes sociales.

El objetivo del sistema es interpretar consultas en lenguaje natural y responder utilizando datos estructurados (publicaciones, métricas, comentarios) almacenados en base de datos.

## Arquitectura general

Flujo de una solicitud:

1. El usuario envía un mensaje al endpoint /chat
2. Se detecta la intención del mensaje
3. El orchestrator decide qué datos consultar
4. Se recuperan publicaciones, métricas, comentarios y contexto RAG
5. Se construye un prompt contextualizado
6. Se ejecuta el modelo de lenguaje
7. Se guarda el historial de la conversación
8. Se retorna la respuesta al cliente

## Estructura del proyecto

```text
.
├── app/
│   ├── api/
│   │   └── chat.py
│   ├── services/
│   │   ├── llm.py
│   │   ├── intent_detector.py
│   │   ├── orchestrator.py
│   │   ├── prompt_builder.py
│   │   └── embeddings.py
│   ├── db/
│   │   ├── database.py
│   │   └── schema.sql
│   ├── utils/
│   │   └── config.py
│   └── data/
│       └── chatbot.db
├── scripts/
│   └── seed_dummy_data.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Requisitos

- Docker
- Docker Compose

## Levantar el proyecto con Docker

Desde la raíz del proyecto ejecutar: docker compose up --build

El servicio quedará disponible en: http://localhost:8000

## Verificación

Health check:

    GET /health

Respuesta esperada:

    {
        "status": "ok",
        "service": "bandurria-backend"
    }

## Documentación de la API

Swagger UI disponible en: http://localhost:8000/docs

## Uso del chatbot

### Endpoint principal

#### POST /chat

Ejemplo de request:

json:

    {
    "message": "¿Cómo va el engagement de mis publicaciones?",
    "session_id": "nico"
    }

Ejemplo de response:

json:

    {
    "session_id": "nico",
    "reply": "El engagement del último post es alto..."
    }

#### Historial de conversación

Obtiene todo el historial asociado a una sesión.

GET /chat/history/{session_id}

Ejemplo: GET /chat/history/nico

Respuesta:

    [
    {
        "role": "user",
        "content": "¿Cómo va el engagement?",
        "created_at": "2026-01-03 03:40:12"
    },
    {
        "role": "assistant",
        "content": "El engagement es alto...",
        "created_at": "2026-01-03 03:40:13"
    }
    ]

### Detección de intención

El sistema detecta automáticamente la intención del usuario, por ejemplo: consultar publicaciones, consultar métricas, analizar comentarios, obtener recomendaciones, preguntas generales
    
Permite consultas compuestas como:
    "Dime cuáles publicaciones tengo y cómo me fue en cada una"

### Capa semántica (Orchestrator)

El orchestrator decide dinámicamente: qué datos consultar, qué tablas usar, si se debe aplicar RAG, cómo estructurar el contexto

Se hizo de esta forma principalmente para no enviar toda la base de datos al modelo en Open AI, reduciendo costos en uso de tokens.

### Base de datos

Se utiliza SQLite para efectos del MVP.

Tablas principales: posts, meta_metrics, meta_comments, messages, embeddings

### Poblar datos de prueba

Para cargar datos dummy: python -m scripts.seed_dummy_data

## API de Publicaciones (Posts)

### Crear publicación

POST /posts

Request JSON:

  {
    "post_id": "post_001",
    "platform": "instagram",
    "caption": "Descuento por tiempo limitado",
    "created_at": "2026-01-03T12:00:00"
  }

Campos

post_id (string): Identificador único del post.
Ejemplo: "post_001", "ig_984312"

platform (string): origen

caption (string): Texto o descripción de la publicación.

created_at (opcional): Fecha de creación en formato ISO 8601 (Si no se envía, se genera automáticamente).

### Listar publicaciones

GET /posts

### Actualizar publicación

PUT /posts/{post_id}

Request JSON:

  {
    "caption": "Nuevo descuento especial"
  }

Campos opcionales, solo se actualizan los enviados.

### Eliminar publicación

DELETE /posts/{post_id}

## API de Métricas

### Crear métrica

POST /metrics

Request JSON:

  {
    "post_id": "post_001",
    "metric_name": "engagement",
    "period": "day",
    "value": 0.34,
    "end_time": "2026-01-02T08:35:35.295979"
  }

Campos

post_id (string): ID del post asociado.

metric_name (string): Nombre de la métrica.

    Valores comunes: "likes", "comments", "shares", "reach", "impressions", "engagement"

period (string): en que periodo se hizo

value (float): Valor numérico de la métrica.

end_time (datetime): fecha

### Listar métricas

GET /metrics

### Actualizar métrica

PUT /metrics/{metric_id}

Request JSON:

  {
    "value": 0.42
  }

### Eliminar métrica

DELETE /metrics/{metric_id}

## API de Comentarios

### Crear comentario

POST /comments

Request JSON:

  {
    "post_id": "post_001",
    "comment_id": "c1",
    "text": "Muy buena oferta",
    "sentiment": "positivo"
    "timestamp": "2026-01-02T08:35:35.295979"
  }

Campos

post_id (string): ID del post asociado.

comment_id (string): ID del comentario.

text (string): Contenido del comentario.

sentiment (string) (opcional): Clasificación de sentimiento.

Valores permitidos: "positivo", "neutral", "negativo", 

timestamp (datetime): fecha de cuando se hizo

### Listar comentarios

GET /comments

### Actualizar comentario

PUT /comments/{comment_id}

Request JSON:

  {
    "text": "Buen precio pero esperaba más",
    "sentiment": "neutral"
  }

Todos los campos son opcionales (pero idealmente incorporarlos).

### Eliminar comentario

DELETE /comments/{comment_id}