<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Home, Settings, ChartNoAxesColumn, UsersRound, Hash, LogOut, MoreVertical, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
} from '@/components/ui/sidebar'
import {
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu'

// Props para controlar el estado en mobile
const props = defineProps<{
  open?: boolean
}>();

const emits = defineEmits<{
  'update:open': [value: boolean]
}>();

const isOpen = computed({
  get: () => props.open ?? false,
  set: (value: boolean) => emits('update:open', value)
});

// Track window width para responsive
const isMobileView = ref(false);

const handleResize = () => {
  isMobileView.value = typeof window !== 'undefined' && window.innerWidth < 768;
};

onMounted(() => {
  handleResize();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

// Menu items.
const items = [
  {
    title: 'Panel',
    url: '#',
    icon: Home,
  },
  {
    title: 'Analíticas',
    url: '#',
    icon: ChartNoAxesColumn,
  },
  {
    title: 'Audiencia',
    url: '#',
    icon: UsersRound,
  },
  {
    title: 'Hashtags',
    url: '#',
    icon: Hash,
  },
  {
    title: 'Configuraciones',
    url: '#',
    icon: Settings,
  },
]

// User data (placeholders)
const user = {
  name: 'Usuario',
  email: 'usuario@example.com',
  status: 'Cuenta Activa',
}

const dropdownOpen = ref(false)

</script>

<template>
  <!-- Sidebar para mobile (modal) -->
  <div
    v-if="isOpen && isMobileView"
    class="fixed inset-y-0 left-0 z-50 w-64 bg-sidebar text-sidebar-foreground border-r border-border flex flex-col md:hidden"
  >
    <!-- Close button -->
    <div class="flex items-center justify-between p-4 border-b border-border">
      <h2 class="font-semibold">Menú</h2>
      <Button
        @click="isOpen = false"
        variant="ghost"
        size="icon"
        class="h-8 w-8"
      >
        <X class="size-5" />
      </Button>
    </div>
    <!-- Rest of sidebar content -->
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Menú</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in items" :key="item.title">
              <SidebarMenuButton as-child @click="isOpen = false">
                <a :href="item.url">
                  <component :is="item.icon" />
                  <span>{{ item.title }}</span>
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>

    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <div class="relative w-full">
            <button
              @click="dropdownOpen = !dropdownOpen"
              class="w-full flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-sidebar-accent transition-colors"
            >
              <UsersRound class="size-4" />
              <div class="grid flex-1 text-left text-sm leading-tight">
                <span class="truncate font-semibold">{{ user.name }}</span>
                <span class="truncate text-xs text-muted-foreground">{{ user.status }}</span>
              </div>
              <MoreVertical class="ml-auto size-4" />
            </button>

            <DropdownMenuContent :open="dropdownOpen" side="top" class="w-56">
              <DropdownMenuItem @click="dropdownOpen = false">
                <span>Perfil</span>
              </DropdownMenuItem>
              <DropdownMenuItem @click="dropdownOpen = false">
                <span>Configuración</span>
              </DropdownMenuItem>
              <DropdownMenuItem @click="dropdownOpen = false">
                <LogOut class="size-4 mr-2" />
                <span>Cerrar sesión</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </div>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  </div>

  <!-- Sidebar para desktop (normal) -->
  <Sidebar class="hidden md:flex">
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg">
            <!-- Contenedor del logo -->
            <div
              class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-secondary text-sidebar-secondary-foreground"
            >
              <!-- Logo -->
              <img
                src="../assets/LOGO_APP.png"
                alt="Logo T-Radar"
                class="h-5 w-5 object-contain"
              />
            </div>
            <!-- Texto -->
            <div class="grid flex-1 text-left text-sm leading-tight">
              <span class="truncate font-semibold">T-Radar</span>
              <span class="truncate text-xs italic">Gestiona tu presencia</span>
            </div>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>

    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Menú</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in items" :key="item.title">
              <SidebarMenuButton as-child>
                <a :href="item.url">
                  <component :is="item.icon" />
                  <span>{{ item.title }}</span>
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>

    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <div class="relative w-full">
            <button
              @click="dropdownOpen = !dropdownOpen"
              class="w-full flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-sidebar-accent transition-colors"
            >
              <UsersRound class="size-4" />
              <div class="grid flex-1 text-left text-sm leading-tight">
                <span class="truncate font-semibold">{{ user.name }}</span>
                <span class="truncate text-xs text-muted-foreground">{{ user.status }}</span>
              </div>
              <MoreVertical class="ml-auto size-4" />
            </button>

            <DropdownMenuContent :open="dropdownOpen" side="top" class="w-56">
              <DropdownMenuItem @click="dropdownOpen = false">
                <span>Perfil</span>
              </DropdownMenuItem>
              <DropdownMenuItem @click="dropdownOpen = false">
                <span>Configuración</span>
              </DropdownMenuItem>
              <DropdownMenuItem @click="dropdownOpen = false">
                <LogOut class="size-4 mr-2" />
                <span>Cerrar sesión</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </div>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  </Sidebar>
</template>
