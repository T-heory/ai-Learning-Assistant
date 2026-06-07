<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{ exercises: any[] }>()

const currentIndex = ref(0)
const userAnswers = ref<Record<number, string>>({})
const submitted = ref<Record<number, boolean>>({})

const currentExercise = computed(() => props.exercises?.[currentIndex.value] || null)
const totalExercises = computed(() => props.exercises?.length || 0)

function selectAnswer(answer: string) {
  if (submitted.value[currentIndex.value]) return
  userAnswers.value[currentIndex.value] = answer
}

function onFillInput(e: Event) {
  if (submitted.value[currentIndex.value]) return
  const target = e.target as HTMLInputElement
  userAnswers.value[currentIndex.value] = target.value
}

function submitAnswer() {
  submitted.value[currentIndex.value] = true
}

function isCorrect(index: number): boolean {
  const ex = props.exercises?.[index]
  return userAnswers.value[index]?.trim().toLowerCase() === ex?.answer?.trim().toLowerCase()
}

function nextExercise() {
  if (currentIndex.value < totalExercises.value - 1) currentIndex.value++
}

function prevExercise() {
  if (currentIndex.value > 0) currentIndex.value--
}
</script>

<template>
  <div class="exercise-panel">
    <div class="exercise-header">
      <span class="exercise-count">{{ currentIndex + 1 }} / {{ totalExercises }}</span>
      <span v-if="currentExercise" :class="['difficulty-tag', currentExercise.difficulty]">
        {{ currentExercise.difficulty === 'easy' ? 'Easy' : currentExercise.difficulty === 'medium' ? 'Medium' : 'Hard' }}
      </span>
    </div>

    <div v-if="currentExercise" class="question-area">
      <p class="question-text">{{ currentExercise.question }}</p>
      <div v-if="currentExercise.type === 'choice' || currentExercise.type === 'multi_choice'" class="options">
        <div v-for="(opt, idx) in currentExercise.options" :key="idx"
          :class="['option-item', {
            selected: userAnswers[currentIndex] === opt,
            correct: submitted[currentIndex] && opt === currentExercise.answer,
            wrong: submitted[currentIndex] && userAnswers[currentIndex] === opt && opt !== currentExercise.answer,
          }]"
          @click="selectAnswer(opt)">
          <span class="option-label">{{ String.fromCharCode(65 + idx) }}</span>
          <span class="option-text">{{ opt }}</span>
          <span v-if="submitted[currentIndex] && opt === currentExercise.answer" class="option-result">✓</span>
        </div>
      </div>
      <div v-if="currentExercise.type === 'fill'" class="fill-area">
        <input class="fill-input" :value="userAnswers[currentIndex] || ''" @input="onFillInput"
          placeholder="Enter answer..." :disabled="submitted[currentIndex]" />
      </div>
    </div>

    <div v-if="!submitted[currentIndex]" class="action-area">
      <button class="submit-btn" :disabled="!userAnswers[currentIndex]" @click="submitAnswer">Submit</button>
    </div>

    <div v-if="submitted[currentIndex] && currentExercise" class="result-area">
      <div :class="['result-banner', isCorrect(currentIndex) ? 'correct' : 'wrong']">
        {{ isCorrect(currentIndex) ? '✅ Correct!' : '❌ Incorrect' }}
      </div>
      <div class="explanation">
        <strong>Explanation:</strong>
        <p>{{ currentExercise.explanation }}</p>
      </div>
    </div>

    <div class="navigation">
      <button class="nav-btn" :disabled="currentIndex === 0" @click="prevExercise">← Previous</button>
      <button class="nav-btn" :disabled="currentIndex === totalExercises - 1" @click="nextExercise">Next →</button>
    </div>
  </div>
</template>

<style scoped>
.exercise-panel { max-width: 600px; }
.exercise-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.exercise-count { font-size: 14px; color: var(--text-secondary); }
.difficulty-tag { font-size: 12px; padding: 2px 8px; border-radius: 4px; }
.difficulty-tag.easy { background: #f0f9eb; color: #67c23a; }
.difficulty-tag.medium { background: #fdf6ec; color: #e6a23c; }
.difficulty-tag.hard { background: #fef0f0; color: #f56c6c; }
.question-text { font-size: 15px; color: var(--text-primary); line-height: 1.6; margin-bottom: 16px; }
.options { display: flex; flex-direction: column; gap: 10px; }
.option-item { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.option-item:hover:not(.correct):not(.wrong) { border-color: var(--primary-color); background: #f0f5ff; }
.option-item.selected { border-color: var(--primary-color); background: #ecf5ff; }
.option-item.correct { border-color: #67c23a; background: #f0f9eb; }
.option-item.wrong { border-color: #f56c6c; background: #fef0f0; }
.option-label { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: #f5f7fa; font-size: 13px; font-weight: 600; }
.option-item.correct .option-label { background: #67c23a; color: #fff; }
.option-item.wrong .option-label { background: #f56c6c; color: #fff; }
.option-text { flex: 1; font-size: 14px; }
.option-result { color: #67c23a; font-weight: bold; }
.fill-input { width: 100%; padding: 10px 14px; border: 1px solid var(--border-color); border-radius: 8px; font-size: 14px; outline: none; }
.fill-input:focus { border-color: var(--primary-color); }
.action-area { margin-top: 16px; }
.submit-btn { background: var(--primary-color); color: #fff; border: none; padding: 10px 24px; border-radius: 8px; font-size: 14px; cursor: pointer; }
.submit-btn:disabled { background: #c0c4cc; cursor: not-allowed; }
.result-area { margin-top: 16px; }
.result-banner { padding: 12px 16px; border-radius: 8px; font-size: 14px; font-weight: 600; margin-bottom: 12px; }
.result-banner.correct { background: #f0f9eb; color: #67c23a; }
.result-banner.wrong { background: #fef0f0; color: #f56c6c; }
.explanation { padding: 12px 16px; background: #f5f7fa; border-radius: 8px; font-size: 14px; line-height: 1.6; }
.explanation p { margin-top: 8px; color: var(--text-secondary); }
.navigation { display: flex; justify-content: space-between; margin-top: 20px; }
.nav-btn { padding: 8px 16px; border: 1px solid var(--border-color); border-radius: 6px; background: #fff; font-size: 13px; color: var(--text-secondary); cursor: pointer; }
.nav-btn:hover:not(:disabled) { border-color: var(--primary-color); color: var(--primary-color); }
.nav-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
