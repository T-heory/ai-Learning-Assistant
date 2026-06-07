<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useChatStore } from '@/stores/chat'

const router = useRouter()
const route = useRoute()
const chatStore = useChatStore()

const navItems = [
  { path: '/chat', label: 'Chat', icon: '💬' },
  { path: '/dashboard', label: 'Profile', icon: '📊' },
  { path: '/learn', label: 'Learn', icon: '📚' },
]

const activeNav = computed(() => route.path)
console.log(activeNav)

function navigate(path: string) {
  router.push(path)
}
</script>

<template>
  <div class="web-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="logo">AI Learning</h2>
      </div>
      <nav class="nav-list">
        <div
          v-for="item in navItems"
          :key="item.path"
          :class="['nav-item', { active: activeNav === item.path }]"
          @click="navigate(item.path)"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </div>
      </nav>
      <div class="sidebar-footer">
        <div class="session-info">
          <span class="session-label">Session</span>
          <span class="session-id">{{ chatStore.sessionId.slice(0, 16) }}...</span>
        </div>
      </div>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.web-layout { display: flex; height: 100vh; background: var(--bg-color); }
.sidebar { width: var(--sidebar-width); background: #fff; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; flex-shrink: 0; }
.sidebar-header { padding: 20px; border-bottom: 1px solid var(--border-color); }
.logo { font-size: 20px; background: linear-gradient(135deg, #409eff, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.nav-list { flex: 1; padding: 12px; display: flex; flex-direction: column; gap: 4px; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s; color: var(--text-secondary); }
.nav-item:hover { background: #f0f5ff; color: var(--primary-color); }
.nav-item.active { background: #ecf5ff; color: var(--primary-color); font-weight: 600; }
.nav-icon { font-size: 18px; }
.nav-label { font-size: 14px; }
.sidebar-footer { padding: 16px 20px; border-top: 1px solid var(--border-color); }
.session-info { display: flex; flex-direction: column; gap: 4px; }
.session-label { font-size: 12px; color: var(--text-placeholder); }
.session-id { font-size: 12px; color: var(--text-secondary); font-family: monospace; }
.main-content { flex: 1; overflow: hidden; display: flex; flex-direction: column; }
</style>
