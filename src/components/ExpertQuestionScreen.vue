<template>
    <div class="question-screen">
      <div class="top-bar">
        <div class="question-progress">{{ currentQuestionIndex + 1 }}/{{ questions.length }}</div>
      </div>
  
      <div class="question-intitule">{{ currentQuestion.question }}</div>
  
      <div class="answers-grid">
        <button
          v-for="(answer, index) in currentQuestion.answers"
          :key="index"
          :class="['answer', selectedAnswer === index ? (index === currentQuestion.correctIndex ? 'correct' : 'wrong') : '']"
          @click="selectAnswer(index)"
          :disabled="answerSelected"
        >
          {{ answer }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const props = defineProps({
    questions: { type: Array, required: true }
  })
  const emit = defineEmits(['finished'])
  
  const currentQuestionIndex = ref(0)
  const currentQuestion = ref(props.questions[0])
  const selectedAnswer = ref(null)
  const answerSelected = ref(false)
  
  function selectAnswer(index) {
    selectedAnswer.value = index
    answerSelected.value = true
  
    setTimeout(() => {
      if (currentQuestionIndex.value + 1 < props.questions.length) {
        currentQuestionIndex.value++
        currentQuestion.value = props.questions[currentQuestionIndex.value]
        selectedAnswer.value = null
        answerSelected.value = false
      } else {
        emit('finished')
      }
    }, 1000)
  }
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
  }
  .correct {
    background-color: #4caf50;
    color: white;
  }
  .wrong {
    background-color: #f44336;
    color: white;
  }
  </style>
  