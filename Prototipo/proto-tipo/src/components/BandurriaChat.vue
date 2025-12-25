<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { MessageCircle, Send, Lightbulb } from 'lucide-vue-next'

interface Message {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
}

const messages = ref<Message[]>([])
const inputValue = ref('')
const showQuickIdeas = ref(true)
const messagesContainer = ref<HTMLElement | null>(null)

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

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const addMessage = (content: string, type: 'user' | 'bot') => {
  const message: Message = {
    id: Date.now().toString(),
    type,
    content,
    timestamp: new Date(),
  }
  messages.value.push(message)
  scrollToBottom()
}

const sendMessage = () => {
  if (inputValue.value.trim()) {
    const userMessage = inputValue.value
    addMessage(userMessage, 'user')
    inputValue.value = ''
    
    // Simular respuesta del bot
    setTimeout(() => {
      addMessage(`Entendido: "${userMessage}". Estoy procesando tu solicitud...`, 'bot')
    }, 1000)
  }
}

const selectQuickIdea = (idea: typeof quickIdeas[0]) => {
  showQuickIdeas.value = false
  addMessage(idea.description, 'user')
  
  // Simular respuesta del bot
  setTimeout(() => {
    addMessage(`Claro, voy a ayudarte con: "${idea.title}". Analizando los datos...`, 'bot')
  }, 1000)
}

const handleKeyPress = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <div class="flex flex-col h-full bg-background border-l border-border">
    <!-- Header -->
    <div class="bg-gradient-to-r from-orange-50 to-orange-100 dark:from-slate-800 dark:to-slate-700 flex flex-col gap-2 p-2 border-b border-border">
      <div class="flex items-center gap-3">
        <MessageCircle class="size-6" style="color: #F18E52" />
        <h1 class="text-lg font-bold text-gray-900 dark:text-white">BandurrIA</h1>
      </div>
      <p class="text-sm italic text-gray-700 dark:text-gray-300 ml-9">Obtén sugerencias personalizadas</p>
    </div>

    <!-- Quick Ideas Section -->
    <div v-if="showQuickIdeas" class="p-4 border-b border-border">
      <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Ideas rápidas</h2>
      <div class="grid grid-cols-1 gap-3">
        <button
          v-for="idea in quickIdeas"
          :key="idea.id"
          @click="selectQuickIdea(idea)"
          class="p-3 rounded-lg border border-border bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-left cursor-pointer flex items-start gap-3"
        >
          <component :is="idea.icon" class="size-5 flex-shrink-0 mt-0.5" style="color: #F18E52" />
          <div class="flex-1">
            <div class="font-medium text-sm text-gray-900 dark:text-white">{{ idea.title }}</div>
            <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">{{ idea.description }}</div>
          </div>
        </button>
      </div>
    </div>

    <!-- Messages Section -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
      <div v-if="messages.length === 0 && !showQuickIdeas" class="flex items-center justify-center h-full">
        <p class="text-gray-500 dark:text-gray-400 text-center">
          Empieza a chatear con BandurrIA
        </p>
      </div>
      
      <div v-for="message in messages" :key="message.id" class="flex gap-3">
        <!-- User Message -->
        <div v-if="message.type === 'user'" class="flex justify-end w-full">
          <div
            class="max-w-xs px-4 py-2 rounded-2xl text-white"
            style="background-color: #F18E52"
          >
            {{ message.content }}
          </div>
        </div>
        
        <!-- Bot Message -->
        <div v-else class="flex justify-start w-full">
          <div class="max-w-xs px-4 py-2 rounded-2xl bg-slate-200 dark:bg-slate-700 text-gray-900 dark:text-white">
            {{ message.content }}
          </div>
        </div>
      </div>
    </div>

    <!-- Footer - Input Section -->
    <div class="border-t border-border p-4 bg-background">
      <div class="flex gap-2">
        <textarea
          v-model="inputValue"
          @keypress="handleKeyPress"
          placeholder="Escribe tu pregunta o prompt..."
          class="chat-textarea flex-1 p-2 rounded-lg border border-border bg-white dark:bg-slate-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none focus:outline-none transition-all"
          rows="3"
        />
        <button
          @click="sendMessage"
          :disabled="!inputValue.trim()"
          class="px-4 py-2 rounded-lg text-white font-medium transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center h-fit"
          style="background-color: #F18E52"
        >
          <Send class="size-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos personalizados para el chat */
.chat-textarea:focus {
  box-shadow: 0 0 0 3px rgba(241, 142, 82, 0.1);
  border-color: #F18E52;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style>
