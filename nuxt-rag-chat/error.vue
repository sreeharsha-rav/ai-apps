<script setup lang="ts">
import type { NuxtError } from "#app";

const props = defineProps({
  error: Object as () => NuxtError,
});
</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen space-y-4">
    <h1 class="text-4xl font-bold text-red-500">
      Error: {{ error.statusCode }}
    </h1>
    <NuxtLink to="/" class="text-gray-800 dark:text-white underline"
      >Go back to home</NuxtLink
    >
  </div>
</template>
