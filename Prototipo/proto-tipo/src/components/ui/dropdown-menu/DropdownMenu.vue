<script setup lang="ts">
import { ref } from 'vue'

const open = ref(false)

defineExpose({
  open,
})
</script>

<template>
  <div class="relative inline-block">
    <slot :open="open" />
  </div>
</template>
