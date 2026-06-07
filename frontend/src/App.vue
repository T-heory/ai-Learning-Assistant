<script setup lang="ts">
import { useDevice } from '@/composables/useDevice'
import WebLayout from '@/layouts/WebLayout.vue'
import MobileLayout from '@/layouts/MobileLayout.vue'

const { isMobile } = useDevice()
</script>

<template>
  <WebLayout v-if="!isMobile" />
  <MobileLayout v-else />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  width: 100%;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
