<template>
  <UDivider class="mt-6" />
  <footer class="flex items-center justify-between gap-2 my-2">
    <div>
      <p class="text-sm text-gray-500">
        Built with
        <a href="https://nuxt.com/" target="_blank" class="text-primary">
          <!-- <img
            src="https://nuxt.com/assets/design-kit/icon-green.svg"
            alt="Nuxt Logo"
            class="inline h-5"
          /> -->
          Nuxt
        </a>
        and
        <a href="https://neon.tech/" target="_blank" class="text-primary">
          <!-- <img
            src="https://neon.tech/favicon/favicon-256x256.png"
            alt="Neon Logo"
            class="inline h-3"
          /> -->
          Neon
        </a>
      </p>
    </div>
    <div class="flex items-center justify-end">
      <UButton
        icon="i-simple-icons-github"
        color="gray"
        variant="ghost"
        to="https://github.com/sreeharsha-rav/ai-apps/tree/main/nuxt-rag-chat"
        target="_blank"
      />
    </div>
  </footer>
</template>
