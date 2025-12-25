<script setup lang="ts">
import { cn } from '@/lib/utils'

interface Props {
  class?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
})

const emits = defineEmits(['click'])
</script>

<template>
  <div
    :class="
      cn(
        'relative flex cursor-pointer select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground disabled:pointer-events-none disabled:opacity-50',
        {
          'opacity-50 cursor-not-allowed': disabled,
        },
        props.class,
      )
    "
    role="menuitem"
    :aria-disabled="disabled"
    @click="!disabled && emits('click')"
  >
    <slot />
  </div>
</template>
