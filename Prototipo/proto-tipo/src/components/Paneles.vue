<script setup lang="ts">
import { TrendingUp, Users, MessageSquare, Flame, Hash, BarChart3 } from 'lucide-vue-next'

// Datos placeholder para gráfico
const weeklyData = [
  { day: 'Lun', engagement: 12 },
  { day: 'Mar', engagement: 19 },
  { day: 'Mié', engagement: 15 },
  { day: 'Jue', engagement: 25 },
  { day: 'Vie', engagement: 22 },
  { day: 'Sáb', engagement: 28 },
  { day: 'Dom', engagement: 20 },
]

const maxEngagement = Math.max(...weeklyData.map(d => d.engagement))
</script>

<template>
  <div class="space-y-4 md:space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">Dashboard principal</h1>
      <p class="text-sm md:text-base text-gray-600 dark:text-gray-400 mt-2">Bienvenido a tu panel de análisis</p>
    </div>

    <!-- Section 1: Métricas Principales (1x2) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
      <!-- Crecimiento -->
      <div class="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-slate-800 dark:to-slate-700 rounded-xl p-6 border border-orange-200 dark:border-orange-900">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-gray-700 dark:text-gray-300 text-sm font-medium">Crecimiento en Redes</p>
            <p class="text-4xl font-bold mt-3" style="color: #F18E52">+15%</p>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">Tu alcance aumentó esta semana</p>
          </div>
          <div class="p-3 bg-orange-200 dark:bg-orange-900 rounded-lg">
            <TrendingUp class="size-6" style="color: #F18E52" />
          </div>
        </div>
      </div>

      <!-- Hitos -->
      <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-xl p-6 border border-blue-200 dark:border-blue-900">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-gray-700 dark:text-gray-300 text-sm font-medium">Hitos Importantes</p>
            <p class="text-4xl font-bold mt-3 text-blue-600 dark:text-blue-400">10K</p>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">Alcanzaste 10 mil seguidores</p>
          </div>
          <div class="p-3 bg-blue-200 dark:bg-blue-900 rounded-lg">
            <Users class="size-6 text-blue-600 dark:text-blue-400" />
          </div>
        </div>
      </div>
    </div>

    <!-- Section 2: Insights (2x2) -->
    <div>
      <h2 class="text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-4">Insights</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
        <!-- Hora Peak -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-900 dark:text-white">Hora Peak Detectada</h3>
            <Flame class="size-5 text-orange-500" />
          </div>
          <p class="text-3xl font-bold" style="color: #F18E52">7 PM</p>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">Tu audiencia es más activa</p>
        </div>

        <!-- Contenido Exitoso -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-900 dark:text-white">Contenido Más Exitoso</h3>
            <BarChart3 class="size-5 text-blue-500" />
          </div>
          <p class="text-3xl font-bold text-blue-600 dark:text-blue-400">Reels</p>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">Mejor desempeño promedio</p>
        </div>

        <!-- Nuevo Segmento -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-900 dark:text-white">Nuevo Segmento</h3>
            <Users class="size-5 text-purple-500" />
          </div>
          <p class="text-3xl font-bold text-purple-600 dark:text-purple-400">18-24 años</p>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">Crecimiento demográfico detectado</p>
        </div>

        <!-- Sugerencia de Trend -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-900 dark:text-white">Trend Sugerido</h3>
            <MessageSquare class="size-5 text-green-500" />
          </div>
          <p class="text-3xl font-bold text-green-600 dark:text-green-400">#TechLife</p>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">Tendencia en crecimiento</p>
        </div>
      </div>
    </div>

    <!-- Section 3: Tus Analíticas -->
    <div>
      <h2 class="text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-4">Tus Analíticas</h2>
      
      <!-- Métricas pequeñas (4x1) -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6">
        <!-- Alcance Total -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <p class="text-gray-600 dark:text-gray-400 text-sm font-medium">Alcance Total</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white mt-3">125K</p>
          <p class="text-xs text-green-600 dark:text-green-400 mt-2">↑ 8% desde la semana pasada</p>
        </div>

        <!-- Tasa de Engagement -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <p class="text-gray-600 dark:text-gray-400 text-sm font-medium">Tasa de Engagement</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white mt-3">5.8%</p>
          <p class="text-xs text-green-600 dark:text-green-400 mt-2">↑ 1.2% desde la semana pasada</p>
        </div>

        <!-- Nuevos Seguidores -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <p class="text-gray-600 dark:text-gray-400 text-sm font-medium">Nuevos Seguidores</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white mt-3">1.2K</p>
          <p class="text-xs text-green-600 dark:text-green-400 mt-2">↑ 340 esta semana</p>
        </div>

        <!-- Frecuencia de Posts -->
        <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <p class="text-gray-600 dark:text-gray-400 text-sm font-medium">Frecuencia de Posts</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white mt-3">4.2</p>
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-2">Posts por semana</p>
        </div>
      </div>

      <!-- Gráfico de Engagement Semanal -->
      <div class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-6">Engagement Semanal</h3>
        
        <!-- Gráfico simple -->
        <div class="flex items-end justify-between h-48 md:h-64 gap-2">
          <div v-for="data in weeklyData" :key="data.day" class="flex-1 flex flex-col items-center justify-end gap-2">
            <!-- Barra -->
            <div
              class="w-full rounded-t-lg transition-all hover:opacity-80 cursor-pointer"
              :style="{
                height: `${(data.engagement / maxEngagement) * 180}px`,
                backgroundColor: '#F18E52',
              }"
              :title="`${data.day}: ${data.engagement}%`"
            />
            <!-- Etiqueta -->
            <p class="text-xs md:text-sm font-medium text-gray-600 dark:text-gray-400">{{ data.day }}</p>
          </div>
        </div>

        <!-- Eje Y indicativo -->
        <div class="mt-4 text-xs text-gray-500 dark:text-gray-500">
          <div>Engagement (%): 0 - {{ maxEngagement }}</div>
        </div>
      </div>
    </div>

    <!-- Section 4: Temas Actuales (2x3) -->
    <div>
      <h2 class="text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-4">Temas Actuales</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        <div v-for="i in 6" :key="i" class="bg-gradient-to-br from-indigo-50 to-indigo-100 dark:from-slate-800 dark:to-slate-700 rounded-xl p-6 border border-indigo-200 dark:border-indigo-900">
          <div class="flex items-center gap-3 mb-3">
            <Hash class="size-5" style="color: #F18E52" />
            <span class="font-semibold text-gray-900 dark:text-white">#TrendingTopic{{ i }}</span>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400">12.5K menciones</p>
          <p class="text-xs text-indigo-600 dark:text-indigo-400 mt-2">↑ Trending en 3 plataformas</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transitions */
</style>
