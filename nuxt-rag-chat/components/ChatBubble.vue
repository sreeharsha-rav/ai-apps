<script setup lang="ts">
import type { Message } from "~/types/message";
const props = defineProps<{
  message: Message;
}>();

const isUser = computed(() => props.message.role === "user");
</script>
<template>
  <div
    :class="[
      'block mt-4 md:mt-6 pb-[7px] clear-both',
      isUser ? 'float-right' : 'float-left',
    ]"
  >
    <div
      :class="[
        'p-2 inline-block break-words',
        isUser
          ? 'bg-green-100 text-gray-800 dark:bg-green-600 dark:text-white  rounded-tl-lg rounded-tr-lg rounded-bl-lg'
          : 'bg-gray-100 text-gray-800  dark:bg-gray-800 dark:text-gray-100 rounded-tr-lg rounded-tl-lg rounded-br-lg',
      ]"
    >
      <!-- Loading Message -->
      <div
        v-if="message.processing"
        class="w-8 h-4 flex items-center justify-center space-x-1"
      >
        <div class="animate-pulse bg-current rounded-full h-1 w-1"></div>
        <div
          class="animate-pulse bg-current rounded-full h-1 w-1 animation-delay-200"
        ></div>
        <div
          class="animate-pulse bg-current rounded-full h-1 w-1 animation-delay-400"
        ></div>
      </div>

      <div v-else>
        {{ message.content }}
      </div>
    </div>
  </div>
</template>
<style scoped>
.animation-delay-200 {
  animation-delay: 200ms;
}
.animation-delay-400 {
  animation-delay: 400ms;
}
</style>
