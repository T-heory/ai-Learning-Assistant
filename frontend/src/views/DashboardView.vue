<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useLearningStore } from '@/stores/learning'

const learningStore = useLearningStore()

onMounted(() => { learningStore.fetchProfile() })

const dimensionLabels: Record<string, string> = {
  knowledge_base: 'Knowledge Base',
  cognitive_style: 'Cognitive Style',
  error_prone: 'Error-prone',
  major_background: 'Background',
  learning_goal: 'Learning Goal',
  pace_preference: 'Pace',
}

const levelColors: Record<string, string> = {
  beginner: '#e6a23c',
  intermediate: '#409eff',
  advanced: '#67c23a',
}

const levelNames: Record<string, string> = {
  beginner: 'Beginner',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
}

const radarData = computed(() => {
  const dims = learningStore.profile?.dimensions || {}
  const levelScore: Record<string, number> = { beginner: 30, intermediate: 60, advanced: 90 }
  return Object.entries(dims).map(([key, val]: [string, any]) => ({
    name: dimensionLabels[key] || key,
    score: levelScore[val.level] || 50,
    level: val.level,
    levelName: levelNames[val.level] || val.level,
    description: val.description,
  }))
})
</script>

<template>
  <div class="dashboard-view">
    <div class="page-header">
      <h2 class="page-title">Learning Profile</h2>
      <p class="page-desc">Dynamic student profile built from conversation, updated as you learn</p>
    </div>

    <div class="profile-summary" v-if="learningStore.profile?.summary">
      <div class="summary-card">
        <span class="summary-icon">📋</span>
        <p class="summary-text">{{ learningStore.profile.summary }}</p>
      </div>
    </div>

    <div v-if="radarData.length === 0" class="empty-profile">
      <div class="empty-icon">📋</div>
      <p class="empty-text">No profile data yet</p>
      <p class="empty-sub">Go to Chat and tell me about your learning background</p>
    </div>

    <div v-else class="dimension-list">
      <div v-for="dim in radarData" :key="dim.name" class="dimension-card">
        <div class="dimension-header">
          <span class="dimension-name">{{ dim.name }}</span>
          <span class="dimension-level" :style="{ color: levelColors[dim.level] || '#999' }">
            {{ dim.levelName }}
          </span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: dim.score + '%', background: levelColors[dim.level] || '#409eff' }"></div>
        </div>
        <p class="dimension-desc">{{ dim.description }}</p>
      </div>
    </div>

    <div v-if="learningStore.profile?.confidence" class="confidence-section">
      <div class="confidence-label">
        Profile Confidence
        <span class="confidence-value">{{ Math.round(learningStore.profile.confidence * 100) }}%</span>
      </div>
      <el-progress :percentage="Math.round(learningStore.profile.confidence * 100)" :stroke-width="8" color="#409eff" />
    </div>
  </div>
</template>

<style scoped>
.dashboard-view { padding: 24px; overflow-y: auto; height: 100%; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 24px; color: var(--text-primary); margin-bottom: 8px; }
.page-desc { font-size: 14px; color: var(--text-secondary); }
.profile-summary { margin-bottom: 20px; }
.summary-card { display: flex; gap: 12px; padding: 16px; background: #ecf5ff; border-radius: 12px; border-left: 4px solid var(--primary-color); }
.summary-icon { font-size: 24px; }
.summary-text { font-size: 14px; color: var(--text-primary); line-height: 1.6; }
.empty-profile { text-align: center; padding: 60px 20px; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-text { font-size: 16px; color: var(--text-secondary); margin-bottom: 8px; }
.empty-sub { font-size: 13px; color: var(--text-placeholder); }
.dimension-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; margin-bottom: 20px; }
.dimension-card { background: #fff; border: 1px solid var(--border-color); border-radius: 12px; padding: 16px; transition: all 0.2s; }
.dimension-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
.dimension-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.dimension-name { font-size: 15px; font-weight: 600; color: var(--text-primary); }
.dimension-level { font-size: 12px; padding: 2px 8px; border-radius: 4px; background: #f5f7fa; }
.progress-bar { height: 6px; background: #f0f0f0; border-radius: 3px; margin-bottom: 10px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
.dimension-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
.confidence-section { padding: 16px; background: #fff; border: 1px solid var(--border-color); border-radius: 12px; }
.confidence-label { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; color: var(--text-secondary); }
.confidence-value { font-weight: 600; color: var(--primary-color); }
@media (max-width: 768px) { .dashboard-view { padding: 16px; } .dimension-list { grid-template-columns: 1fr; } }
</style>
