<script setup>
const props = defineProps({
  content: {
    type: Object,
    required: true,
  },
});

const isUser = computed(() => props.content.role === "user");
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
      <div
        v-if="content.processing"
        class="w-6 h-6 flex items-center justify-center"
      >
        <div class="animate-pulse bg-current rounded-full h-2 w-2"></div>
      </div>
      <div v-else>
        {{ content.content }}
      </div>
    </div>
  </div>
</template>
