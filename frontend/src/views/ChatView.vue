<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useLearningStore } from '@/stores/learning'
import { useDevice } from '@/composables/useDevice'
const chatStore = useChatStore()
const learningStore = useLearningStore()
const { isMobile } = useDevice()

const inputText = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

async function handleSend() {
  const text = inputText.value.trim()
  if (!text) return
  inputText.value = ''
  await chatStore.sendMessage(text)
  await scrollToBottom()
  await learningStore.fetchProfile()
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

const exampleMessages = [
  "I'm a CS sophomore wanting to learn machine learning",
  "I'm an accounting freshman with zero Python experience",
  "I'm a product manager wanting to learn data analysis",
]

function fillExample(text: string) {
  inputText.value = text
  handleSend()
}

onMounted(() => {
  learningStore.fetchProfile()
})
</script>

<template>
  <div class="chat-view">
    <div ref="messagesContainer" class="message-list">
      <div v-if="chatStore.messages.length === 0" class="empty-state">
        <div class="empty-icon">🎓</div>
        <h2 class="empty-title">Start Your Learning Journey</h2>
        <p class="empty-desc">Tell me about your background and goals, and I'll create a personalized learning plan for you.</p>
        <div class="examples">
          <div v-for="(msg, idx) in exampleMessages" :key="idx" class="example-item" @click="fillExample(msg)">
            <span class="example-icon">💡</span>
            <span>{{ msg }}</span>
          </div>
        </div>
      </div>

      <div v-for="msg in chatStore.messages" :key="msg.id" :class="['message-item', msg.role === 'user' ? 'user-msg' : 'ai-msg']">
        <div class="message-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
        <div class="message-bubble">
          <div class="message-content" v-html="msg.content.replace(/\n/g, '<br/>')"></div>
          <div v-if="msg.streaming" class="streaming-indicator">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          </div>
        </div>
      </div>

      <div v-if="chatStore.isLoading && chatStore.messages[chatStore.messages.length - 1]?.role === 'user'" class="loading-msg">
        <div class="message-avatar">🤖</div>
        <div class="loading-bubble">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        </div>
      </div>
    </div>

    <div class="input-area">
      <div class="input-wrapper">
        <textarea
          v-model="inputText"
          class="chat-input"
          :placeholder="isMobile ? 'Type a message...' : 'Tell me what you want to learn...'"
          @keydown="handleKeydown"
          :disabled="chatStore.isLoading"
          rows="1"
        />
        <button class="send-btn" :disabled="!inputText.trim() || chatStore.isLoading" @click="handleSend">
          🚀
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-view { display: flex; flex-direction: column; height: 100%; background: #fff; }
.message-list { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 16px; }
.empty-state { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; padding: 40px 20px; }
.empty-icon { font-size: 64px; margin-bottom: 8px; }
.empty-title { font-size: 22px; color: var(--text-primary); }
.empty-desc { font-size: 14px; color: var(--text-secondary); text-align: center; max-width: 300px; }
.examples { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; width: 100%; max-width: 400px; }
.example-item { display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: #f5f7fa; border-radius: 10px; cursor: pointer; transition: all 0.2s; font-size: 14px; color: var(--text-secondary); }
.example-item:hover { background: #ecf5ff; color: var(--primary-color); transform: translateY(-1px); }
.message-item { display: flex; gap: 10px; max-width: 80%; }
.message-item.user-msg { align-self: flex-end; flex-direction: row-reverse; }
.message-avatar { font-size: 28px; flex-shrink: 0; }
.message-bubble { padding: 12px 16px; border-radius: 12px; font-size: 14px; line-height: 1.6; }
.user-msg .message-bubble { background: #409eff; color: #fff; border-bottom-right-radius: 4px; }
.ai-msg .message-bubble { background: #f5f7fa; color: var(--text-primary); border-bottom-left-radius: 4px; }
.message-content { word-break: break-word; }
.loading-msg { display: flex; gap: 10px; align-items: center; }
.loading-bubble { padding: 16px 20px; background: #f5f7fa; border-radius: 12px; display: flex; gap: 4px; }
.dot { width: 6px; height: 6px; background: #c0c4cc; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; } 40% { transform: scale(1); opacity: 1; } }
.streaming-indicator { display: flex; gap: 3px; margin-top: 8px; }
.streaming-indicator .dot { width: 4px; height: 4px; }
.input-area { padding: 12px 16px; border-top: 1px solid var(--border-color); background: #fff; }
.input-wrapper { display: flex; gap: 8px; align-items: flex-end; }
.chat-input { flex: 1; border: 1px solid var(--border-color); border-radius: 10px; padding: 10px 14px; font-size: 14px; outline: none; resize: none; font-family: inherit; line-height: 1.5; max-height: 120px; transition: border-color 0.2s; }
.chat-input:focus { border-color: var(--primary-color); }
.chat-input:disabled { background: #f5f7fa; cursor: not-allowed; }
.send-btn { width: 44px; height: 44px; border: none; border-radius: 10px; background: var(--primary-color); color: #fff; font-size: 20px; cursor: pointer; transition: all 0.2s; flex-shrink: 0; }
.send-btn:hover:not(:disabled) { background: #66b1ff; }
.send-btn:disabled { background: #c0c4cc; cursor: not-allowed; }
</style>
