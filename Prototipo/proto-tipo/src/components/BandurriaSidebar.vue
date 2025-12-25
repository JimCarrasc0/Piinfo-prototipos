<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { MessageCircle, Send, Lightbulb, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
} from '@/components/ui/sidebar'

interface Message {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
}

const messages = ref<Message[]>([])
const inputValue = ref('')
const showQuickIdeas = ref(true)
const openChatMobile = ref(false)
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

// User data (placeholders)
// Placeholder para futuro uso

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
  <!-- Botón trigger para mobile -->
  <div v-if="!openChatMobile" class="fixed bottom-6 right-6 z-40 md:hidden">
    <Button
      @click="openChatMobile = true"
      class="h-14 w-14 rounded-full shadow-lg"
      style="background-color: #F18E52"
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
          <div class="max-w-xs px-3 py-2 rounded-2xl bg-slate-200 dark:bg-slate-700 text-gray-900 dark:text-white text-sm">
            {{ message.content }}
          </div>
        </div>
      </div>
    </div>

    <!-- Footer - Input Section -->
    <div class="p-4 border-t border-border flex gap-2 flex-col">
      <textarea
        v-model="inputValue"
        @keypress="handleKeyPress"
        placeholder="Escribe tu pregunta..."
        class="chat-textarea flex-1 p-2 rounded-lg border border-border bg-white dark:bg-slate-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none focus:outline-none transition-all text-sm"
        rows="2"
      />
      <button
        @click="sendMessage"
        :disabled="!inputValue.trim()"
        class="px-3 py-2 rounded-lg text-white font-medium transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center h-fit self-end"
        style="background-color: #F18E52"
      >
        <Send class="size-4" />
      </button>
    </div>
  </div>

  <!-- Chat sidebar para desktop -->
  <Sidebar side="right" class="border-l border-border hidden lg:flex">
    <!-- Header -->
    <SidebarHeader>
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-3">
          <MessageCircle class="size-6" style="color: #F18E52" />
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
          <component :is="idea.icon" class="size-4 flex-shrink-0 mt-0.5" style="color: #F18E52" />
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
        
        <div v-for="message in messages" :key="message.id" class="flex gap-2 px-2">
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
            <div class="max-w-xs px-3 py-2 rounded-2xl bg-slate-200 dark:bg-slate-700 text-gray-900 dark:text-white text-sm">
              {{ message.content }}
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
          placeholder="Escribe tu pregunta..."
          class="chat-textarea flex-1 p-2 rounded-lg border border-border bg-white dark:bg-slate-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none focus:outline-none transition-all text-sm"
          rows="2"
        />
        <button
          @click="sendMessage"
          :disabled="!inputValue.trim()"
          class="px-3 py-2 rounded-lg text-white font-medium transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center h-fit self-end"
          style="background-color: #F18E52"
        >
          <Send class="size-4" />
        </button>
      </div>
    </SidebarFooter>
  </Sidebar>
</template>

<style scoped>
.chat-textarea:focus {
  box-shadow: 0 0 0 3px rgba(241, 142, 82, 0.1);
  border-color: #F18E52;
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
