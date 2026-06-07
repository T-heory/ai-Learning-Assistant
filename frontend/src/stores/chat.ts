import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { createSessionId } from '@/api'

export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: number
  streaming?: boolean
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const isLoading = ref(false)
  const sessionId = ref(createSessionId())
  const error = ref<string | null>(null)

  async function sendMessage(content: string) {
    if (!content.trim() || isLoading.value) return
    error.value = null

    const userMsg: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: content.trim(),
      timestamp: Date.now(),
    }
    messages.value.push(userMsg)

    const aiMsg: Message = {
      id: `msg_${Date.now() + 1}`,
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      streaming: true,
    }
    messages.value.push(aiMsg)

    isLoading.value = true

    try {
      const response = await api.chat(content, sessionId.value) as any
      aiMsg.content = response.reply
      aiMsg.streaming = false
    } catch (err: any) {
      aiMsg.content = 'Sorry, I encountered an error. Please check if the backend service is running.'
      aiMsg.streaming = false
      error.value = err.message || 'Request failed'
    } finally {
      isLoading.value = false
    }
  }

  function clearMessages() {
    messages.value = []
    sessionId.value = createSessionId()
  }

  function setSessionId(id: string) {
    sessionId.value = id
  }

  return {
    messages, isLoading, sessionId, error,
    sendMessage, clearMessages, setSessionId,
  }
})
