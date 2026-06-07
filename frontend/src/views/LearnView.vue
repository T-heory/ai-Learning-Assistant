<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLearningStore } from '@/stores/learning'
import { useChatStore } from '@/stores/chat'
import { useDevice } from '@/composables/useDevice'

const learningStore = useLearningStore()
const chatStore = useChatStore()
const { isMobile } = useDevice()

const topicInput = ref('')
const activeTab = ref('document')

const tabs = [
  { key: 'document', label: '📄 Document' },
  { key: 'mindmap', label: '🧠 Mind Map' },
  { key: 'exercises', label: '📝 Exercises' },
  { key: 'readings', label: '📚 Readings' },
  { key: 'practice', label: '💻 Practice' },
]

async function handleGenerate() {
  if (!topicInput.value.trim()) return
  await learningStore.generateResources(topicInput.value.trim())
  await learningStore.planPath(topicInput.value.trim())
  activeTab.value = 'document'
}

async function generateFromChat() {
  const lastMsg = chatStore.messages.filter(m => m.role === 'user').pop()
  if (lastMsg) {
    topicInput.value = lastMsg.content.slice(0, 50)
    await handleGenerate()
  }
}

onMounted(() => {})
</script>

<template>
  <div class="learn-view">
    <div class="topic-section">
      <h2 class="page-title">Learning Center</h2>
      <p class="page-desc">Enter a topic to generate personalized learning resources</p>
      <div class="topic-input-row">
        <input v-model="topicInput" class="topic-input" placeholder="e.g. Python list comprehensions" @keyup.enter="handleGenerate" />
        <button class="generate-btn" :disabled="!topicInput.trim() || learningStore.resourcesLoading" @click="handleGenerate">
          {{ learningStore.resourcesLoading ? '⏳ Generating...' : '🚀 Generate' }}
        </button>
      </div>
      <button v-if="chatStore.messages.length > 0 && !topicInput" class="from-chat-btn" @click="generateFromChat">
        💡 Generate from recent chat
      </button>
    </div>

    <div v-if="learningStore.learningPath" class="path-preview">
      <PathTimeline :path="learningStore.learningPath" />
    </div>

    <div v-if="learningStore.resources" class="resources-section">
      <div :class="['tab-nav', { 'tab-nav-mobile': isMobile }]">
        <button v-for="tab in tabs" :key="tab.key" :class="['tab-btn', { active: activeTab === tab.key }]" @click="activeTab = tab.key">
          {{ tab.label }}
        </button>
      </div>

      <div v-if="activeTab === 'document' && learningStore.resources.document" class="tab-content">
        <ResourceCard :title="learningStore.resources.document.title" type="document">
          <div class="markdown-content" v-html="learningStore.resources.document.content"></div>
        </ResourceCard>
      </div>

      <div v-if="activeTab === 'mindmap' && learningStore.resources.mindmap" class="tab-content">
        <ResourceCard :title="learningStore.resources.mindmap.title" type="mindmap">
          <MindMap :code="learningStore.resources.mindmap.mermaid_code" />
        </ResourceCard>
      </div>

      <div v-if="activeTab === 'exercises' && learningStore.resources.exercises" class="tab-content">
        <ResourceCard title="Exercises" type="exercises">
          <ExercisePanel :exercises="learningStore.resources.exercises" />
        </ResourceCard>
      </div>

      <div v-if="activeTab === 'readings' && learningStore.resources.readings" class="tab-content">
        <ResourceCard title="Further Reading" type="readings">
          <div class="readings-list">
            <div v-for="(item, idx) in learningStore.resources.readings" :key="idx" class="reading-item">
              <h4 class="reading-title">{{ item.title }}</h4>
              <p class="reading-summary">{{ item.summary }}</p>
              <p v-if="item.reason" class="reading-reason">💡 {{ item.reason }}</p>
            </div>
          </div>
        </ResourceCard>
      </div>

      <div v-if="activeTab === 'practice' && learningStore.resources.practice" class="tab-content">
        <ResourceCard :title="learningStore.resources.practice.title" type="practice">
          <div class="practice-content">
            <p class="practice-desc">{{ learningStore.resources.practice.description }}</p>
            <h4>Steps</h4>
            <ol class="practice-steps">
              <li v-for="(step, idx) in learningStore.resources.practice.steps" :key="idx">{{ step }}</li>
            </ol>
            <h4>Code</h4>
            <pre class="code-block"><code>{{ learningStore.resources.practice.code }}</code></pre>
            <p v-if="learningStore.resources.practice.expected_output"><strong>Expected output:</strong> {{ learningStore.resources.practice.expected_output }}</p>
          </div>
        </ResourceCard>
      </div>
    </div>

    <div v-if="!learningStore.resources && !learningStore.resourcesLoading" class="empty-state">
      <div class="empty-icon">📖</div>
      <p class="empty-text">Enter a topic to generate personalized resources</p>
      <p class="empty-sub">Content will be tailored to your learning profile</p>
    </div>

    <div v-if="learningStore.resourcesLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>AI is generating learning resources for you...</p>
    </div>
  </div>
</template>

<style scoped>
.learn-view { padding: 24px; overflow-y: auto; height: 100%; }
.page-title { font-size: 24px; color: var(--text-primary); margin-bottom: 8px; }
.page-desc { font-size: 14px; color: var(--text-secondary); margin-bottom: 16px; }
.topic-section { margin-bottom: 20px; }
.topic-input-row { display: flex; gap: 10px; }
.topic-input { flex: 1; padding: 10px 16px; border: 1px solid var(--border-color); border-radius: 8px; font-size: 14px; outline: none; transition: border-color 0.2s; }
.topic-input:focus { border-color: var(--primary-color); }
.generate-btn { padding: 10px 20px; background: var(--primary-color); color: #fff; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; white-space: nowrap; transition: all 0.2s; }
.generate-btn:hover:not(:disabled) { background: #66b1ff; }
.generate-btn:disabled { background: #c0c4cc; cursor: not-allowed; }
.from-chat-btn { margin-top: 10px; padding: 8px 16px; background: none; border: 1px dashed var(--border-color); border-radius: 8px; font-size: 13px; color: var(--text-secondary); cursor: pointer; transition: all 0.2s; }
.from-chat-btn:hover { border-color: var(--primary-color); color: var(--primary-color); }
.path-preview { margin-bottom: 20px; }
.resources-section { background: #fff; border: 1px solid var(--border-color); border-radius: 12px; overflow: hidden; }
.tab-nav { display: flex; overflow-x: auto; border-bottom: 1px solid var(--border-color); background: #fafafa; }
.tab-nav-mobile { -webkit-overflow-scrolling: touch; }
.tab-btn { padding: 12px 20px; border: none; background: none; font-size: 14px; color: var(--text-secondary); cursor: pointer; white-space: nowrap; border-bottom: 2px solid transparent; transition: all 0.2s; }
.tab-btn:hover { color: var(--primary-color); background: #f0f5ff; }
.tab-btn.active { color: var(--primary-color); border-bottom-color: var(--primary-color); font-weight: 600; }
.tab-content { padding: 20px; }
.readings-list { display: flex; flex-direction: column; gap: 16px; }
.reading-item { padding: 16px; background: #f9f9f9; border-radius: 8px; border-left: 3px solid var(--primary-color); }
.reading-title { font-size: 15px; color: var(--text-primary); margin-bottom: 8px; }
.reading-summary { font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 8px; }
.reading-reason { font-size: 12px; color: #e6a23c; }
.practice-content { font-size: 14px; line-height: 1.6; }
.practice-desc { color: var(--text-secondary); margin-bottom: 16px; }
.practice-steps { padding-left: 20px; margin-bottom: 16px; }
.practice-steps li { margin-bottom: 8px; color: var(--text-primary); }
.code-block { background: #f5f7fa; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; border: 1px solid var(--border-color); }
.empty-state { text-align: center; padding: 60px 20px; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-text { font-size: 16px; color: var(--text-secondary); margin-bottom: 8px; }
.empty-sub { font-size: 13px; color: var(--text-placeholder); }
.loading-state { text-align: center; padding: 60px 20px; }
.loading-spinner { width: 40px; height: 40px; border: 3px solid #f0f0f0; border-top-color: var(--primary-color); border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 768px) { .learn-view { padding: 16px; } .topic-input-row { flex-direction: column; } .tab-btn { padding: 10px 14px; font-size: 13px; } .tab-content { padding: 12px; } }
</style>
