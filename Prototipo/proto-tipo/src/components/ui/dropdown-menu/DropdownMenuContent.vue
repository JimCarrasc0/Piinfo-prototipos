<script setup lang="ts">
import { cn } from '@/lib/utils'

interface Props {
  side?: 'top' | 'bottom' | 'left' | 'right'
  class?: string
  open?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  side: 'bottom',
  open: false,
})
</script>

<template>
  <div
    v-if="open"
    class="absolute z-50 rounded-md border bg-popover text-popover-foreground shadow-md"
    :class="[
      cn(
        'min-w-32 overflow-hidden bg-background border border-border shadow-lg rounded-md',
        {
          'top-full mt-2': side === 'bottom',
          'bottom-full mb-2': side === 'top',
          'left-full ml-2': side === 'right',
          'right-full mr-2': side === 'left',
        },
        props.class,
      ),
    ]"
  >
    <slot />
  </div>
</template>
