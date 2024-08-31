<script setup lang="ts">
import { useChatStore } from "@/stores/chat";
const chatStore = useChatStore();

const messages = computed(() => chatStore.messages);
const hasMessages = computed(() => chatStore.hasMessages);

const handleSuggestionClick = (suggestion: string) => {
  chatStore.sendMessage(suggestion);
};

const beforeEnter = (el) => {
  el.style.opacity = 0;
  el.style.transform = "translateY(20px)";
};

const enter = (el, done) => {
  const delay = el.dataset.index * 150;
  setTimeout(() => {
    el.style.transition = "all 0.3s ease";
    el.style.opacity = 1;
    el.style.transform = "translateY(0)";

    if (el.classList.contains("user-bubble")) {
      el.style.transform += " translateX(-20px)";
    } else if (el.classList.contains("assistant-bubble")) {
      el.style.transform += " translateX(20px)";
    }

    el.addEventListener("transitionend", done);
  }, delay);
};

const leave = (el, done) => {
  el.style.opacity = 0;
  el.style.transform = "translateY(20px)";
  el.addEventListener("transitionend", done);
};
</script>
<template>
  <div
    class="pl-8 pr-16 overflow-y-auto h-[calc(64vh)] scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-800 scrollbar-track-transparent"
  >
    <!-- Chat messages with transitions -->
    <TransitionGroup
      name="chat-bubble"
      tag="div"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <ChatBubble
        v-for="(message, index) in messages"
        :key="message.id"
        :message="message"
        :data-index="index"
      />
    </TransitionGroup>

    <!-- Show prompt suggestions when there are no messages -->
    <Transition name="fade">
      <div v-if="!hasMessages" class="mt-4">
        <h3 class="text-lg font-medium mb-2">Suggested Prompts:</h3>
        <PromptSuggestions @suggestion-click="handleSuggestionClick" />
      </div>
    </Transition>
  </div>
</template>
<style scoped>
.chat-bubble-move {
  transition: all 0.5s ease;
}

.user-bubble {
  transform-origin: bottom right;
}

.assistant-bubble {
  transform-origin: bottom left;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
