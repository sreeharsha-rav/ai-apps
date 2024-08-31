<script setup lang="ts">
const colorMode = useColorMode();

function toggleColorMode() {
  colorMode.preference = colorMode.value === "dark" ? "light" : "dark";
}
</script>
<template>
  <header class="flex items-center justify-between p-4">
    <h1 class="text-2xl font-bold text-primary">NeoChat</h1>
    <button
      @click="toggleColorMode"
      class="p-1 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600"
    >
      <span v-if="$colorMode.value === 'light'">☀️</span>
      <span v-else>🌙</span>
    </button>
  </header>
</template>
