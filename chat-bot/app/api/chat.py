from fastapi import APIRouter, HTTPException          # Router y manejo de errores HTTP
from pydantic import BaseModel                        # Validación de datos
from typing import Optional                           # Tipos opcionales

from app.db.database import get_db                    # Acceso a la base de datos
from app.services.llm import run_llm
from app.services.intent_detector import detect_intent
from app.services.orchestrator import build_context
from app.services.prompt_builder import build_prompt

router = APIRouter(tags=["chat"])                     # Router del módulo chat

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str


class ChatMessage(BaseModel):
    role: str
    content: str
    created_at: str

"""
DESCRIPCIÓN:
Endpoint principal del chatbot (API: interfaz HTTP).
Recibe un mensaje, detecta intención, obtiene contexto,
construye el prompt y consulta al LLM.
"""
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        db = get_db()

        session_id = payload.session_id or "default"

        intent = detect_intent(payload.message)

        context = build_context(
            message=payload.message,
            intent_data=intent
        )

        prompt_text = build_prompt(
            context=context,
            user_message=payload.message
        )

        messages = [
            {"role": "user", "content": prompt_text}
        ]

        reply = run_llm(messages)

        db.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, "user", payload.message),
        )
        db.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, "assistant", reply),
        )
        db.commit()

        return ChatResponse(
            session_id=session_id,
            reply=reply
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando mensaje: {str(e)}"
        )

"""
DESCRIPCIÓN:
Obtiene el historial completo de una sesión.
Se usa para rehidratar el chat en el frontend (UI: interfaz de usuario).
"""
@router.get("/history/{session_id}", response_model=list[ChatMessage])
async def get_chat_history(session_id: str):
    db = get_db()

    rows = db.execute(
        """
        SELECT role, content, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY created_at ASC
        """,
        (session_id,),
    ).fetchall()

    return [
        {
            "role": row["role"],
            "content": row["content"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]
