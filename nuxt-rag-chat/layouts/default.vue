<template>
  <div
    class="mt-10 min-h-[70%] max-w-4xl mx-auto flex flex-col bg-white dark:bg-gray-900 shadow-2xl border border-gray-200 dark:border-gray-800 rounded-lg"
  >
    <!-- Header -->
    <Header />

    <!-- Main Content -->
    <slot />

    <div class="px-4">
      <!-- Chat Input -->
      <ChatInput />
      <!-- Footer -->
      <Footer />
    </div>
  </div>
</template>
