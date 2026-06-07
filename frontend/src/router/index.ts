import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/chat' },
    {
      path: '/chat',
      name: 'Chat',
      component: () => import('@/views/ChatView.vue'),
      meta: { title: 'Chat', icon: 'ChatDotSquare' },
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { title: 'Dashboard', icon: 'DataAnalysis' },
    },
    {
      path: '/learn',
      name: 'Learn',
      component: () => import('@/views/LearnView.vue'),
      meta: { title: 'Learn', icon: 'Reading' },
    },
  ],
})

export default router
