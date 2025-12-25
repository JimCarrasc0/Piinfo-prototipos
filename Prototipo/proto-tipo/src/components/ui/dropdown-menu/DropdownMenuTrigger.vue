<script setup lang="ts">
interface Props {
  asChild?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  asChild: false,
})

const emits = defineEmits(['click'])
</script>

<template>
  <button
    v-if="!asChild"
    @click="emits('click')"
    class="flex items-center gap-2 w-full"
  >
    <slot />
  </button>
  <div v-else @click="emits('click')" class="flex items-center gap-2 w-full cursor-pointer">
    <slot />
  </div>
</template>
