<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ path: any }>()

const steps = computed(() => props.path?.steps || [])
const title = computed(() => props.path?.title || 'Learning Path')
</script>

<template>
  <div class="path-timeline">
    <div class="path-header">
      <h3 class="path-title">🗺️ {{ title }}</h3>
      <div class="path-meta">
        <span class="meta-item">⏱ {{ path?.total_hours || '?' }} hours total</span>
        <span class="meta-item">📅 {{ path?.total_days || '?' }} days</span>
      </div>
    </div>

    <div v-if="path?.prerequisites?.length" class="prerequisites">
      <span class="prereq-label">Prerequisites:</span>
      <span v-for="(prereq, idx) in path.prerequisites" :key="idx" class="prereq-tag">{{ prereq }}</span>
    </div>

    <div class="timeline">
      <div v-for="(step, idx) in steps" :key="idx" :class="['timeline-item', step.status || 'pending']">
        <div class="timeline-node">
          <div class="node-dot" :class="step.status || 'pending'"></div>
          <div v-if="idx < steps.length - 1" class="node-line"></div>
        </div>
        <div class="timeline-content">
          <div class="step-header">
            <span class="step-number">Step {{ step.step }}</span>
            <span class="step-phase">{{ step.phase }}</span>
            <span class="step-duration">⏱ {{ step.duration }}</span>
          </div>
          <h4 class="step-objective">{{ step.objective }}</h4>
          <div class="step-key-points">
            <span v-for="(point, pidx) in step.key_points" :key="pidx" class="key-point">{{ point }}</span>
          </div>
          <p class="step-desc">{{ step.description }}</p>
          <div v-if="step.resource_types" class="step-resources">
            <span v-for="(res, ridx) in step.resource_types" :key="ridx" class="resource-tag">
              {{ res === 'document' ? '📄 Doc' : res === 'mindmap' ? '🧠 Mindmap' : res === 'exercises' ? '📝 Ex' : res === 'readings' ? '📚 Read' : res === 'practice' ? '💻 Code' : res }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="path?.tips?.length" class="tips-section">
      <h4 class="tips-title">💡 Tips</h4>
      <ul class="tips-list">
        <li v-for="(tip, idx) in path.tips" :key="idx">{{ tip }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.path-timeline { background: #fff; border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; }
.path-header { margin-bottom: 16px; }
.path-title { font-size: 18px; color: var(--text-primary); margin-bottom: 8px; }
.path-meta { display: flex; gap: 16px; }
.meta-item { font-size: 13px; color: var(--text-secondary); }
.prerequisites { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; padding: 12px; background: #f5f7fa; border-radius: 8px; }
.prereq-label { font-size: 13px; color: var(--text-secondary); font-weight: 600; }
.prereq-tag { font-size: 12px; padding: 2px 8px; background: #ecf5ff; color: var(--primary-color); border-radius: 4px; }
.timeline { position: relative; }
.timeline-item { display: flex; gap: 16px; margin-bottom: 8px; }
.timeline-node { display: flex; flex-direction: column; align-items: center; width: 20px; flex-shrink: 0; }
.node-dot { width: 12px; height: 12px; border-radius: 50%; border: 2px solid var(--border-color); background: #fff; flex-shrink: 0; }
.node-dot.completed { background: #67c23a; border-color: #67c23a; }
.node-dot.in_progress { background: var(--primary-color); border-color: var(--primary-color); box-shadow: 0 0 0 3px rgba(64,158,255,0.2); }
.node-line { width: 2px; flex: 1; background: var(--border-color); min-height: 20px; }
.timeline-content { flex: 1; padding-bottom: 20px; }
.step-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
.step-number { font-size: 12px; padding: 2px 8px; background: #f5f7fa; color: var(--text-secondary); border-radius: 4px; }
.step-phase { font-size: 14px; font-weight: 600; color: var(--text-primary); }
.step-duration { font-size: 12px; color: var(--text-secondary); }
.step-objective { font-size: 14px; color: var(--text-primary); margin-bottom: 8px; }
.step-key-points { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px; }
.key-point { font-size: 12px; padding: 2px 8px; background: #f0f9eb; color: #67c23a; border-radius: 4px; }
.step-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 8px; }
.step-resources { display: flex; flex-wrap: wrap; gap: 6px; }
.resource-tag { font-size: 12px; padding: 2px 8px; background: #ecf5ff; color: var(--primary-color); border-radius: 4px; }
.tips-section { margin-top: 20px; padding: 16px; background: #fdf6ec; border-radius: 8px; border: 1px solid #faecd8; }
.tips-title { font-size: 14px; color: #e6a23c; margin-bottom: 8px; }
.tips-list { padding-left: 20px; }
.tips-list li { font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 4px; }
@media (max-width: 768px) { .path-timeline { padding: 12px; } }
</style>
