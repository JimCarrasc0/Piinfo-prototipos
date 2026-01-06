<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { MessageCircle, Send, Lightbulb, X, Loader2, AlertCircle } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
} from '@/components/ui/sidebar'
import {
  sendMessage as chatSendMessage,
  getChatHistory,
  getOrCreateSessionId,
} from '@/lib/chatService'

interface Message {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
  isLoading?: boolean
}

const messages = ref<Message[]>([])
const inputValue = ref('')
const showQuickIdeas = ref(true)
const openChatMobile = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const sessionId = ref<string>('')
const isLoadingMessage = ref(false)
const errorMessage = ref<string | null>(null)

const quickIdeas = [
  {
    id: '1',
    title: 'Analizar Tendencias',
    description: 'Analiza las tendencias actuales en redes sociales',
    icon: Lightbulb,
  },
  {
    id: '2',
    title: 'Optimizar Contenido',
    description: 'Obtén recomendaciones para optimizar tu contenido',
    icon: Lightbulb,
  },
  {
    id: '3',
    title: 'Nuevas Estrategias',
    description: 'Descubre estrategias innovadoras para tu marca',
    icon: Lightbulb,
  },
]

/**
 * Carga el historial de chat al inicializar el componente
 */
const loadChatHistory = async () => {
  try {
    const history = await getChatHistory(sessionId.value)
    if (history && history.length > 0) {
      messages.value = history.map((msg) => ({
        id: Date.now().toString() + Math.random(),
        type: msg.role === 'user' ? 'user' : 'bot',
        content: msg.content,
        timestamp: new Date(msg.created_at),
      }))
      showQuickIdeas.value = false
      scrollToBottom()
    }
  } catch (error) {
    console.error('Error loading chat history:', error)
    // No mostrar error al usuario si es la primera vez
  }
}

/**
 * Se ejecuta cuando el componente está montado
 */
onMounted(() => {
  sessionId.value = getOrCreateSessionId()
  loadChatHistory()
})

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const addMessage = (content: string, type: 'user' | 'bot', isLoading = false) => {
  const message: Message = {
    id: Date.now().toString() + Math.random(),
    type,
    content,
    timestamp: new Date(),
    isLoading,
  }
  messages.value.push(message)
  scrollToBottom()
}

/**
 * Envía un mensaje al chatbot backend
 */
const sendMessage = async () => {
  if (!inputValue.value.trim() || isLoadingMessage.value) return

  const userMessage = inputValue.value
  addMessage(userMessage, 'user')
  inputValue.value = ''
  isLoadingMessage.value = true
  errorMessage.value = null
  showQuickIdeas.value = false

  // Agregar mensaje de carga
  const loadingMessageId = `loading_${Date.now()}`
  messages.value.push({
    id: loadingMessageId,
    type: 'bot',
    content: 'Procesando tu solicitud...',
    timestamp: new Date(),
    isLoading: true,
  })
  await scrollToBottom()

  try {
    const response = await chatSendMessage(userMessage, sessionId.value)

    // Remover mensaje de carga
    messages.value = messages.value.filter((m) => m.id !== loadingMessageId)

    // Agregar respuesta del bot
    addMessage(response.reply, 'bot')
  } catch (error) {
    // Remover mensaje de carga
    messages.value = messages.value.filter((m) => m.id !== loadingMessageId)

    const errorMsg =
      error instanceof Error ? error.message : 'Error desconocido del servidor'
    errorMessage.value = errorMsg
    addMessage(
      `⚠️ Error: ${errorMsg}. Intenta de nuevo.`,
      'bot'
    )
  } finally {
    isLoadingMessage.value = false
  }
}

const selectQuickIdea = (idea: (typeof quickIdeas)[0]) => {
  showQuickIdeas.value = false
  sendMessage.call({ inputValue: { value: idea.description } })
  inputValue.value = idea.description
  sendMessage()
}

const handleKeyPress = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <!-- Botón trigger para mobile -->
  <div v-if="!openChatMobile" class="fixed bottom-6 right-6 z-40 md:hidden">
    <Button
      @click="openChatMobile = true"
      class="h-14 w-14 rounded-full shadow-lg btn-chat-trigger"
    >
      <MessageCircle class="size-6 text-white" />
    </Button>
  </div>

  <!-- Modal overlay para mobile -->
  <div
    v-if="openChatMobile"
    class="fixed inset-0 bg-black/50 z-40 md:hidden"
    @click="openChatMobile = false"
  />

  <!-- Chat content para mobile (sin usar Sidebar component) -->
  <div
    v-if="openChatMobile"
    class="fixed inset-y-0 right-0 z-50 w-80 bg-white dark:bg-slate-950 border-l border-border md:hidden flex flex-col shadow-lg"
  >
    <!-- Close button -->
    <div class="flex items-center justify-between p-4 border-b border-border">
      <h1 class="text-lg font-bold text-gray-900 dark:text-white">BandurrIA</h1>
      <Button
        @click="openChatMobile = false"
        variant="ghost"
        size="icon"
        class="h-8 w-8"
      >
        <X class="size-5" />
      </Button>
    </div>

    <!-- Messages Section -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3">
      <div v-if="messages.length === 0 && !showQuickIdeas" class="flex items-center justify-center py-8">
        <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
          Empieza a chatear con BandurrIA
        </p>
      </div>
      
      <!-- Quick Ideas Section -->
      <div v-if="showQuickIdeas" class="space-y-2">
        <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300">Ideas rápidas</h2>
        <button
          v-for="idea in quickIdeas"
          :key="idea.id"
          @click="selectQuickIdea(idea)"
          class="p-2 rounded-lg border border-border bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-left cursor-pointer flex items-start gap-2 w-full"
        >
          <component :is="idea.icon" class="size-4 flex-shrink-0 mt-0.5" style="color: #F18E52" />
          <div class="flex-1 min-w-0">
            <div class="font-medium text-xs text-gray-900 dark:text-white truncate">{{ idea.title }}</div>
            <div class="text-xs text-gray-600 dark:text-gray-400 mt-0.5 line-clamp-2">{{ idea.description }}</div>
          </div>
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="flex items-start gap-2 px-3 py-2 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900/30">
        <AlertCircle class="size-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
        <p class="text-xs text-red-600 dark:text-red-400">{{ errorMessage }}</p>
      </div>

      <!-- Messages -->
      <div v-for="message in messages" :key="message.id" class="flex gap-2">
        <!-- User Message -->
        <div v-if="message.type === 'user'" class="flex justify-end w-full">
          <div
            class="max-w-xs px-3 py-2 rounded-2xl text-white text-sm"
            style="background-color: #F18E52"
          >
            {{ message.content }}
          </div>
        </div>
        
        <!-- Bot Message -->
        <div v-else class="flex justify-start w-full">
          <div class="max-w-xs px-3 py-2 rounded-2xl bg-slate-200 dark:bg-slate-700 text-gray-900 dark:text-white text-sm flex items-center gap-2">
            <span v-if="message.isLoading">
              <Loader2 class="size-4 animate-spin" />
            </span>
            <span>{{ message.content }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer - Input Section -->
    <div class="p-4 border-t border-border flex gap-2 flex-col">
      <textarea
        v-model="inputValue"
        @keypress="handleKeyPress"
        :disabled="isLoadingMessage"
        placeholder="Escribe tu pregunta..."
        class="chat-textarea flex-1 p-2 rounded-lg border border-border bg-white dark:bg-slate-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none focus:outline-none transition-all text-sm disabled:opacity-50"
        rows="2"
      />
      <button
        @click="sendMessage"
        :disabled="!inputValue.trim() || isLoadingMessage"
        class="px-3 py-2 rounded-lg text-white font-medium transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center h-fit self-end"
        style="background-color: #F18E52"
      >
        <Loader2 v-if="isLoadingMessage" class="size-4 animate-spin" />
        <Send v-else class="size-4" />
      </button>
    </div>
  </div>

  <!-- Chat sidebar para desktop -->
  <Sidebar side="right" class="border-l border-border hidden lg:flex">
    <!-- Header -->
    <SidebarHeader>
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-3">
          <MessageCircle class="size-6 icon-primary" />
          <h1 class="text-lg font-bold text-gray-900 dark:text-white">BandurrIA</h1>
        </div>
        <p class="text-sm italic text-gray-700 dark:text-gray-300 ml-9">Obtén sugerencias personalizadas</p>
      </div>
    </SidebarHeader>

    <!-- Quick Ideas Section -->
    <div v-if="showQuickIdeas" class="px-4 py-3 border-b border-border">
      <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Ideas rápidas</h2>
      <div class="grid grid-cols-1 gap-2">
        <button
          v-for="idea in quickIdeas"
          :key="idea.id"
          @click="selectQuickIdea(idea)"
          class="p-2 rounded-lg border border-border bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-left cursor-pointer flex items-start gap-2"
        >
          <component :is="idea.icon" class="size-4 flex-shrink-0 mt-0.5 icon-primary" />
          <div class="flex-1 min-w-0">
            <div class="font-medium text-xs text-gray-900 dark:text-white truncate">{{ idea.title }}</div>
            <div class="text-xs text-gray-600 dark:text-gray-400 mt-0.5 line-clamp-2">{{ idea.description }}</div>
          </div>
        </button>
      </div>
    </div>

    <!-- Messages Section -->
    <SidebarContent>
      <div ref="messagesContainer" class="flex flex-col gap-3 py-2">
        <div v-if="messages.length === 0 && !showQuickIdeas" class="flex items-center justify-center py-8">
          <p class="text-xs text-gray-500 dark:text-gray-400 text-center px-2">
            Empieza a chatear con BandurrIA
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="flex items-start gap-2 px-3 py-2 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900/30 mx-2">
          <AlertCircle class="size-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
          <p class="text-xs text-red-600 dark:text-red-400">{{ errorMessage }}</p>
        </div>
        
        <div v-for="message in messages" :key="message.id" class="flex gap-2 px-2">
          <!-- User Message -->
          <div v-if="message.type === 'user'" class="flex justify-end w-full">
            <div class="max-w-xs px-3 py-2 rounded-2xl text-white text-sm chat-user-message">
              {{ message.content }}
            </div>
          </div>
          
          <!-- Bot Message -->
          <div v-else class="flex justify-start w-full">
            <div class="max-w-xs px-3 py-2 rounded-2xl chat-bot-message flex items-center gap-2">
              <span v-if="message.isLoading">
                <Loader2 class="size-4 animate-spin" />
              </span>
              <span>{{ message.content }}</span>
            </div>
          </div>
        </div>
      </div>
    </SidebarContent>

    <!-- Footer - Input Section -->
    <SidebarFooter>
      <div class="flex gap-2 flex-col">
        <textarea
          v-model="inputValue"
          @keypress="handleKeyPress"
          :disabled="isLoadingMessage"
          placeholder="Escribe tu pregunta..."
          class="chat-textarea flex-1 p-2 rounded-lg border border-border bg-white dark:bg-slate-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none focus:outline-none transition-all text-sm disabled:opacity-50"
          rows="2"
        />
        <button
          @click="sendMessage"
          :disabled="!inputValue.trim() || isLoadingMessage"
          class="px-3 py-2 rounded-lg text-white font-medium transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center h-fit self-end btn-chat-send"
        >
          <Loader2 v-if="isLoadingMessage" class="size-4 animate-spin" />
          <Send v-else class="size-4" />
        </button>
      </div>
    </SidebarFooter>
  </Sidebar>
</template>

<style scoped>
/* ============================================================================
   ESTILOS DEL CHAT - BandurriaSidebar
   
   Este componente utiliza variables CSS del archivo main.css para mantener
   consistencia con el diseño general. Los colores pueden modificarse en:
   src/assets/main.css
   
   Clases CSS disponibles:
   - .btn-chat-trigger: Botón flotante para abrir chat en mobile
   - .chat-user-message: Estilos para mensajes del usuario
   - .chat-bot-message: Estilos para mensajes del bot
   - .btn-chat-send: Botón para enviar mensajes
   ============================================================================ */

/* Botón flotante para abrir chat (mobile) */
.btn-chat-trigger {
  background-color: var(--button-primary-bg);
  color: var(--button-primary-text);
  box-shadow: var(--shadow-heavy);
}

.btn-chat-trigger:hover {
  opacity: var(--button-hover-opacity);
}

/* Mensajes del usuario - fondo naranja */
.chat-user-message {
  background-color: var(--chat-user-bg);
  color: var(--chat-user-text);
}

/* Mensajes del bot - fondo gris */
.chat-bot-message {
  background-color: var(--chat-bot-bg);
  color: var(--chat-bot-text);
}

/* Botón para enviar mensajes */
.btn-chat-send {
  background-color: var(--button-primary-bg);
  color: var(--button-primary-text);
}

.btn-chat-send:hover:not(:disabled) {
  opacity: var(--button-hover-opacity);
}

/* Textarea del chat - enfoque */
.chat-textarea:focus {
  box-shadow: 0 0 0 3px var(--chat-button-hover);
  border-color: var(--chat-input-border);
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #999;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
