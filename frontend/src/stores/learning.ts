import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'
import { useChatStore } from './chat'

export const useLearningStore = defineStore('learning', () => {
  const profile = ref<Record<string, any>>({})
  const profileLoading = ref(false)
  const resources = ref<Record<string, any> | null>(null)
  const resourcesLoading = ref(false)
  const learningPath = ref<Record<string, any> | null>(null)
  const pathLoading = ref(false)
  const evaluation = ref<Record<string, any> | null>(null)
  const evalLoading = ref(false)

  async function fetchProfile() {
    const chatStore = useChatStore()
    profileLoading.value = true
    try {
      const res = await api.getProfile(chatStore.sessionId) as any
      profile.value = res.profile || {}
    } catch (err) {
      console.error('Fetch profile error:', err)
    } finally {
      profileLoading.value = false
    }
  }

  async function generateResources(topic: string) {
    const chatStore = useChatStore()
    resourcesLoading.value = true
    try {
      const res = await api.generateResources(topic, chatStore.sessionId) as any
      resources.value = res.output_data?.result || res
    } catch (err) {
      console.error('Generate resources error:', err)
    } finally {
      resourcesLoading.value = false
    }
  }

  async function planPath(topic: string) {
    const chatStore = useChatStore()
    pathLoading.value = true
    try {
      const res = await api.planPath(topic, chatStore.sessionId) as any
      learningPath.value = res.output_data?.result || res
    } catch (err) {
      console.error('Plan path error:', err)
    } finally {
      pathLoading.value = false
    }
  }

  async function evaluate(answers: any[] = []) {
    const chatStore = useChatStore()
    evalLoading.value = true
    try {
      const res = await api.evaluate(chatStore.sessionId, answers) as any
      evaluation.value = res.output_data?.result || res
    } catch (err) {
      console.error('Evaluate error:', err)
    } finally {
      evalLoading.value = false
    }
  }

  return {
    profile, profileLoading,
    resources, resourcesLoading,
    learningPath, pathLoading,
    evaluation, evalLoading,
    fetchProfile, generateResources, planPath, evaluate,
  }
})
