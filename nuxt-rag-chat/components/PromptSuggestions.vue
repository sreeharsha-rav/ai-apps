<script setup lang="ts">
const suggestions = ref<string[]>([
  "Is Tailwind CSS a free library?",
  "What's the latest Tailwind CSS version?",
  "Is it a utility-class based CSS framework?",
]);
</script>
<template>
  <div class="flex flex-wrap gap-2">
    <button
      v-for="prompt in suggestions"
      type="button"
      class="mb-2.5 me-1.5 py-2 px-3 inline-flex justify-center items-center gap-x-2 rounded-lg border border-green-600 text-primary align-middle focus:outline-none text-sm hover:text-green-400 hover:border-green-400 focus:text-primary focus:border-primary"
    >
      <span>{{ prompt }}</span>
    </button>
  </div>
</template>
