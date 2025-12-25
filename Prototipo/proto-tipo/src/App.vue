<script setup>
import { ref } from 'vue';
import { Menu } from 'lucide-vue-next';
import { Button } from '@/components/ui/button';
import Barra2 from '@/components/Barra2.vue';
import Paneles from '@/components/Paneles.vue';
import BandurriaSidebar from '@/components/BandurriaSidebar.vue';
import { SidebarProvider } from './components/ui/sidebar';

// Estado para controlar el sidebar del menú en mobile
const showMenuMobile = ref(false);
</script>

<template>
  <SidebarProvider>
    <!-- Overlay para mobile cuando está abierto el menú -->
    <div
      v-if="showMenuMobile"
      class="fixed inset-0 bg-black/50 z-40 md:hidden"
      @click="showMenuMobile = false"
    />

    <!-- Sidebar Izquierda - Navegación -->
    <Barra2 :open="showMenuMobile" @update:open="showMenuMobile = $event" />
    
    <!-- Contenido Principal -->
    <main class="flex-1 flex flex-col lg:flex-row">
      <div class="flex-1 flex flex-col">
        <!-- Header con botón del menú en mobile -->
        <div class="flex items-center gap-2 p-4 md:hidden border-b border-border">
          <Button
            @click="showMenuMobile = true"
            variant="ghost"
            size="icon"
            class="h-8 w-8"
          >
            <Menu class="size-5" />
          </Button>
        </div>
        <div class="flex-1 p-4 md:p-6 overflow-auto">
          <!-- Dashboard Principal -->
          <Paneles />
        </div>
      </div>
    </main>

    <!-- Sidebar Derecha - Chat -->
    <BandurriaSidebar />
  </SidebarProvider>
</template>

<style scoped>
main {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

@media (min-width: 1024px) {
  main {
    flex-direction: row;
  }
}
</style>
