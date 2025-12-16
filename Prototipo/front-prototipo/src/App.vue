<script setup>
import Sidebar from './componentes/sidebar.vue'
</script>

<template>
  <section class="layout">
  <div class="sidebar">
    <Sidebar />
  </div>
  <div class="body">2</div>
</section>

</template>

<style scoped>
.layout {
  width: 100%;

  display: grid;
  grid:
    "sidebar body" 1fr
    / auto 1fr;
  gap: 8px;
}

.sidebar { grid-area: sidebar; }
.body { grid-area: body; }
</style>
