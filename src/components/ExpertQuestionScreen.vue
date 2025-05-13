<template>
  <div class="question-screen">
    <div v-if="!showFeedback">
      <div class="top-bar">
        <div class="question-progress">{{ currentQuestionIndex + 1 }}/{{ questions.length }}</div>
      </div>

      <div class="question-intitule">{{ currentQuestion.question }}</div>

      <div class="answers-grid">
        <button
          v-for="(answer, index) in currentQuestion.answers"
          :key="index"
          :class="[
            'answer',
            (answerSelected && index === currentQuestion.correctIndex) ? 'correct' : '',
            (selectedAnswer === index && index !== currentQuestion.correctIndex) ? 'wrong' : '',
            (answerSelected && index !== selectedAnswer && index !== currentQuestion.correctIndex) ? 'fade-out' : ''
          ]"
          @click="selectAnswer(index)"
          :disabled="answerSelected"
        >
          {{ answer }}
        </button>
      </div>
    </div>

    <div v-else class="feedback-screen">
      <img :src="`/images/${currentQuestion.feedback.image}`" class="feedback-image" />
      <div class="feedback-text">{{ currentQuestion.feedback.text }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ questions: Array })
const emit = defineEmits(['finished'])

const currentQuestionIndex = ref(0)
const currentQuestion = ref(props.questions[0])
const selectedAnswer = ref(null)
const answerSelected = ref(false)
const score = ref(0)
const showFeedback = ref(false)

function selectAnswer(index) {
  if (answerSelected.value) return
  selectedAnswer.value = index
  answerSelected.value = true

  if (index === currentQuestion.value.correctIndex) {
    score.value++
  }

  setTimeout(() => {
    showFeedback.value = true
    setTimeout(() => {
      showFeedback.value = false
      if (currentQuestionIndex.value + 1 < props.questions.length) {
        currentQuestionIndex.value++
        currentQuestion.value = props.questions[currentQuestionIndex.value]
        selectedAnswer.value = null
        answerSelected.value = false
      } else {
        emit('finished', score.value)
      }
    }, 10000)
  }, 5000)
}

function selectAnswerFromHardware(letter) {
  const index = ['A', 'B', 'C', 'D'].indexOf(letter.toUpperCase())
  if (index !== -1 && !answerSelected.value) {
    selectAnswer(index)
  }
}

defineExpose({ selectAnswerFromHardware })
</script>

<style scoped>
.question-screen {
  font-size: 18px;
  text-align: center;
}
.answers-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 20px;
}
.answer {
  padding: 12px;
  font-size: 16px;
  transition: opacity 1s ease, transform 1s ease;
}
.correct {
  background-color: #4caf50;
  color: white;
}
.wrong {
  background-color: #f44336;
  color: white;
}
.fade-out {
  opacity: 0;
  transform: scale(0.9);
  pointer-events: none;
}
.feedback-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.feedback-image {
  max-width: 300px;
  margin-bottom: 20px;
}
.feedback-text {
  font-size: 18px;
  font-weight: bold;
  max-width: 80%;
}
</style>
