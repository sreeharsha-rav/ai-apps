<script setup lang="ts">
//TODO: Change suggested prompts for Neon DB
const suggestions = ref<string[]>([
  "What is Neon?",
  "What are some features of Neon?",
  "Can I use Neon to build AI applications?",
]);

const emit = defineEmits(["suggestion-click"]);

const handleClick = (suggestion: string) => {
  emit("suggestion-click", suggestion);
};
</script>
<template>
  <div class="flex flex-wrap gap-2">
    <button
      v-for="prompt in suggestions"
      :key="prompt"
      type="button"
      class="mb-2.5 me-1.5 py-2 px-3 inline-flex justify-center items-center gap-x-2 rounded-lg border border-green-600 text-primary align-middle focus:outline-none text-sm hover:text-green-400 hover:border-green-400 focus:text-primary focus:border-primary"
      @click="handleClick(prompt)"
    >
      <span>{{ prompt }}</span>
    </button>
  </div>
</template>
