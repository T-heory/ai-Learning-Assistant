<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import mermaid from 'mermaid'

const props = defineProps<{ code: string }>()

const svgContainer = ref<HTMLDivElement | null>(null)
const renderError = ref<string | null>(null)

onMounted(() => {
  mermaid.initialize({
    startOnLoad: false,
    theme: 'default',
    securityLevel: 'loose',
    themeVariables: {
      primaryColor: '#409eff',
      primaryTextColor: '#303133',
      primaryBorderColor: '#409eff',
      lineColor: '#dcdfe6',
      secondaryColor: '#ecf5ff',
      tertiaryColor: '#f5f7fa',
    },
  })
  renderChart()
})

watch(() => props.code, () => { renderChart() })

async function renderChart() {
  if (!props.code || !svgContainer.value) return
  renderError.value = null
  try {
    const id = 'mermaid-' + Date.now()
    const { svg } = await mermaid.render(id, props.code)
    svgContainer.value.innerHTML = svg
  } catch (err: any) {
    console.error('Mermaid render error:', err)
    renderError.value = 'Failed to render mind map. Please try again.'
  }
}
</script>

<template>
  <div class="mindmap-wrapper">
    <div v-if="renderError" class="error-msg">⚠️ {{ renderError }}</div>
    <div ref="svgContainer" class="mermaid-container" :class="{ 'is-loading': !code }">
      <div v-if="!code" class="placeholder">Waiting for mind map data...</div>
    </div>
  </div>
</template>

<style scoped>
.mindmap-wrapper { width: 100%; overflow-x: auto; }
.mermaid-container { min-height: 200px; display: flex; justify-content: center; align-items: center; }
.mermaid-container :deep(svg) { max-width: 100%; height: auto; }
.placeholder { color: var(--text-placeholder); font-size: 14px; }
.error-msg { padding: 12px; color: var(--danger-color); background: #fef0f0; border-radius: 8px; margin-bottom: 12px; font-size: 14px; }
.is-loading { opacity: 0.5; }
</style>
