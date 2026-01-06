# Piinfo-prototipos

sigan este esquema para los commit pls
[Sección (Front|back|chat|etc)] comentario
[Sección] [Asunto (fix|bug|corrección|cambio)] comentario

## 🚀 Quick Start - Docker (Recomendado)

### Windows
```shell
docker-start.bat
```

### macOS / Linux
```shell
bash docker-start.sh
```

**Esto inicia**:
- ✅ Frontend: http://localhost:5173
- ✅ Backend: http://localhost:8000
- ✅ Documentación API: http://localhost:8000/docs

Para más detalles, ver [DOCKER_SETUP.md](DOCKER_SETUP.md)

---

## Stack

### Front-End: Vue.js (v3.5.25) + Vite

**Local (sin Docker)**:
```shell
cd Prototipo/proto-tipo
pnpm install
pnpm dev
```

**Con Docker**:
```shell
docker-compose up proto-tipo-frontend
```

### Back-End: FastAPI (Python)

**Local**:
```shell
cd chat-bot
docker compose up --build
```

**Con docker-compose general**:
```shell
docker-compose up tradar-chatbot
```

## Scraper

para ejecutar el scraper seguir esta estructura

```shell
python scraper.py [usuario a scrapear] [cookie del usuario scraper]
```
### Obtención cookie
Abrir instagram, y entrar a opciones de desarrollador, la cookie la encuentras en el almacenamiento local.
![alt text](https://github.com/JimCarrasc0/Piinfo-prototipos/blob/main/captura%20cookie.png "Imagen Cookie")

este scraper entrega un documento `publicaciones.json` que sigue el siguiente formato


```json
[
  {
    "id_publicacion": "id_numerico",
    "descripcion": "blabla...",
    "likes": 750,
    "comentarios": 80,
    "tipo_publicacion": "Sidecar (Múltiples imágenes)",
    "fecha_publicacion": "2025-08-19 21:53:43"
  },
  ...
]
```

y por consola muestra lo siguiente


```shell
INSTAGRAM PUBLICATION SCRAPER
================================================================================
Consultando perfil: usuario
✓ Datos obtenidos correctamente

RESUMEN DE PUBLICACIONES
================================================================================
Total de publicaciones: 16

Distribución por tipo:
  Sidecar (Múltiples imágenes): 2 (12.5%)
  Video: 1 (6.2%)
  IGTV: 3 (18.8%)
  ...

Total de likes: 1,234
Total de comentarios: 89

Promedio de likes por publicación: 77.1
Promedio de comentarios por publicación: 5.6

PRIMERAS 3 PUBLICACIONES:
--------------------------------------------------------------------------------

Publicación 1:
  ID: id_numerico
  Tipo: Sidecar (Múltiples imágenes)
  Fecha: 2025-08-19 21:53:43
  Likes: 75 | Comentarios: 0
  Descripción: blabla...

✓ Publicaciones guardadas en: publicaciones.json
✓ Total de publicaciones: 16

✓ Tiempo total de ejecución: 1.23 segundos

✓ Proceso completado exitosamente!
✓ Archivo generado: publicaciones.json
================================================================================
```


