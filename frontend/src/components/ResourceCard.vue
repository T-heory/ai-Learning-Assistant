<script setup lang="ts">
defineProps<{
  title: string
  type: 'document' | 'mindmap' | 'exercises' | 'readings' | 'practice'
}>()

const typeNames: Record<string, string> = {
  document: 'Document',
  mindmap: 'Mind Map',
  exercises: 'Exercises',
  readings: 'Readings',
  practice: 'Practice',
}
</script>

<template>
  <div class="resource-card">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>
      <span class="card-type">{{ typeNames[type] || type }}</span>
    </div>
    <div class="card-body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.resource-card { background: #fff; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0; }
.card-title { font-size: 18px; color: var(--text-primary); }
.card-type { font-size: 12px; padding: 3px 10px; background: #ecf5ff; color: var(--primary-color); border-radius: 4px; }
.card-body { min-height: 60px; }
</style>
