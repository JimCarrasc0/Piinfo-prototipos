/**
 * Chat Service
 * Maneja la comunicación con el backend del chatbot
 * 
 * URLs soportadas:
 * - Desarrollo local: http://localhost:8000/chat
 * - Docker (frontend): /chat (proxy a través de Nginx)
 * - Producción: https://api.example.com/chat (configurar en .env)
 */

// En Docker, el frontend se comunica a través del proxy de Nginx
// En desarrollo local, se comunica directamente a localhost:8000
const CHAT_API_URL = typeof window !== 'undefined' && window.location.hostname === 'localhost'
  ? 'http://localhost:8000/chat'
  : '/chat'

export interface ChatRequest {
  message: string
  session_id: string
}

export interface ChatResponse {
  session_id: string
  reply: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ChatHistory {
  messages: ChatMessage[]
}

/**
 * Genera una ID de sesión única para el usuario
 * Formato: timestamp + número aleatorio
 */
export const generateSessionId = (): string => {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
}

/**
 * Recupera la sesión guardada en localStorage o crea una nueva
 */
export const getOrCreateSessionId = (): string => {
  const stored = localStorage.getItem('chatSessionId')
  if (stored) {
    return stored
  }
  const newId = generateSessionId()
  localStorage.setItem('chatSessionId', newId)
  return newId
}

/**
 * Envía un mensaje al chatbot y recibe la respuesta
 * @param message - Mensaje del usuario
 * @param sessionId - ID de sesión del usuario
 * @returns Promise con la respuesta del chatbot
 * @throws Error si la request falla
 */
export const sendMessage = async (
  message: string,
  sessionId: string
): Promise<ChatResponse> => {
  const payload: ChatRequest = {
    message,
    session_id: sessionId,
  }

  const response = await fetch(`${CHAT_API_URL}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: 'Error desconocido del servidor',
    }))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  return await response.json()
}

/**
 * Recupera el historial de chat para una sesión específica
 * @param sessionId - ID de sesión del usuario
 * @returns Promise con el historial de mensajes
 * @throws Error si la request falla
 */
export const getChatHistory = async (
  sessionId: string
): Promise<ChatMessage[]> => {
  const response = await fetch(`${CHAT_API_URL}/history/${sessionId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: 'Error al recuperar historial',
    }))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  const data = await response.json()
  // El backend devuelve un array de mensajes o un objeto con propiedad 'messages'
  return Array.isArray(data) ? data : data.messages || []
}
