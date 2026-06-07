<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()

const tabs = [
  { path: '/chat', label: 'Chat', icon: 'chat-o' },
  { path: '/dashboard', label: 'Profile', icon: 'chart-trending-o' },
  { path: '/learn', label: 'Learn', icon: 'bookshelf-o' },
]

const activeTab = computed(() => {
  const idx = tabs.findIndex(t => t.path === route.path)
  return idx >= 0 ? idx : 0
})

function onTabChange(index: number) {
  router.push(tabs[index].path)
}
</script>

<template>
  <div class="mobile-layout">
    <div class="mobile-content">
      <router-view />
    </div>
    <van-tabbar
      :value="activeTab"
      @change="onTabChange"
      active-color="#409eff"
      border
    >
      <van-tabbar-item v-for="tab in tabs" :key="tab.path" :icon="tab.icon">
        {{ tab.label }}
      </van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<style scoped>
.mobile-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-color);
}
.mobile-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
