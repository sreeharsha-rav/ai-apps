<script setup lang="ts">
import ChatBubble from "~/components/ChatBubble.vue";

const emptyWindow = ref(false);

const toggleSuggestions = () => {
  emptyWindow.value = !emptyWindow.value;
};

// Your messages logic here
const messages = ref([
  { id: 1, role: "user", content: "Hello!" },
  { id: 2, role: "assistant", content: "Hi there! How can I help you today?" },
  { id: 3, role: "user", content: "I have a question about Neon." },
  { id: 4, role: "assistant", content: "Sure! What do you want to know?" },
  { id: 5, role: "user", content: "Is Neon a free library?" },
  {
    id: 6,
    role: "assistant",
    content: "Yes, Neon is a free and open-source library.",
  },
  { id: 7, role: "user", content: "That's great! Thanks for the information." },
  {
    id: 8,
    role: "assistant",
    content:
      "You're welcome! If you have any more questions, feel free to ask.",
  },
  { id: 9, role: "user", content: "Actually, I have one more question." },
  { id: 10, role: "assistant", content: "Sure, go ahead. I'm here to help." },
  { id: 11, role: "user", content: "Can Neon be used with Vue.js?" },
  {
    id: 12,
    role: "assistant",
    content: "Absolutely! Neon is designed to work seamlessly with Vue.js.",
  },
  { id: 13, role: "user", content: "That's great! I'm excited to try it out." },
  {
    id: 14,
    role: "assistant",
    content:
      "I'm sure you'll love it! Let me know if you need any assistance while using Neon with Vue.js.",
  },
  { id: 15, role: "user", content: "Thank you, I appreciate your help." },
  { id: 16, role: "assistant", content: "You're welcome! Have a great day!" },
  { id: 17, role: "user", content: "You too!" },
]);
</script>
<template>
  <div
    class="pl-8 pr-16 overflow-y-auto h-[calc(64vh)] scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-800 scrollbar-track-transparent"
  >
    <!-- Show prompt suggestions when the chat window is empty -->
    <div v-if="emptyWindow">
      <PromptSuggestions />
    </div>

    <!-- Chat messages -->
    <ChatBubble
      v-for="message in messages"
      :key="message.id"
      :content="message"
    />
  </div>
</template>
