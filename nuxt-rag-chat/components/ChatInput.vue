<script setup lang="ts">
import { useChatStore } from "@/stores/chat";
const chatStore = useChatStore();
const input = ref<string>("");

const sendInput = async () => {
  // If the input is empty, return
  if (input.value.trim() === "") return;

  // Send the message
  try {
    await chatStore.sendMessage(input.value.trim());
  } catch (error) {
    console.error(`Failed to send message: ${error}`);
  }
  input.value = "";
};
</script>
<template>
  <div class="inline-flex gap-2 w-full p-4 justify-center">
    <!-- Textarea -->
    <UTextarea
      color="gray"
      v-model="input"
      placeholder="Ask me anything about Neon..."
      class="flex-grow z-10 w-full resize-none"
      @keydown.enter.prevent="sendInput"
    />
    <!-- Send Button -->
    <button
      type="button"
      class="inline-flex shrink-0 justify-center items-center size-8 rounded-lg text-white bg-green-500 hover:bg-green-400 focus:z-10 focus:outline-none focus:bg-green-500"
      @click="sendInput"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="lucide lucide-send"
      >
        <path d="m22 2-7 20-4-9-9-4Z" />
        <path d="M22 2 11 13" />
      </svg>
    </button>
    <!-- End Send Button -->
  </div>
</template>
