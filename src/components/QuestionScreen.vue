<template>
  <div class="question-screen">
    <div class="top-bar">
      <div class="question-progress">{{ currentQuestionIndex + 1 }}/{{ totalQuestions }}</div>
      <div class="timer">{{ timer }}s</div>
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
import { ref, onMounted, watch } from 'vue'

// Props
const props = defineProps({
  selectedTheme: { type: String, required: true },
  selectedQuestionCount: { type: Number, required: true },
  selectedEra: { type: String, required: true }
})

const questions = ref([])
const currentQuestion = ref({})
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const answerSelected = ref(false)
const timer = ref(60)
const totalQuestions = ref(0)
let countdown = null

// Watch sur selectedEra pour recharger les questions quand l'époque change
watch(() => props.selectedEra, async (newEra) => {
  console.log(`L'époque a changé, nouvelle époque : ${newEra}`)
  await loadQuestions()
})

onMounted(async () => {
  await loadQuestions()
})

async function loadQuestions() {
  try {
    // Vérifier quelle époque est sélectionnée
    console.log(`Chargement des questions pour l'époque : ${props.selectedEra}, thème : ${props.selectedTheme}`)
    
    // Charger les questions selon l'époque
    const res = await fetch(`/data/questions_${props.selectedEra}.json`)
    if (!res.ok) {
      throw new Error('Erreur lors du chargement du fichier JSON')
    }
    const data = await res.json()

    // Vérifier que le thème est dans les données
    const selectedQuestions = data[props.selectedTheme] || []
  
    questions.value = selectedQuestions.sort(() => 0.5 - Math.random()).slice(0, props.selectedQuestionCount)
    totalQuestions.value = questions.value.length
    currentQuestion.value = questions.value[0]
    startTimer()
  } catch (error) {
    console.error('Erreur de chargement des questions :', error)
  }
}

function startTimer() {
  countdown = setInterval(() => {
    timer.value--
    if (timer.value <= 0) {
      clearInterval(countdown)
      showCorrectAnswer()
    }
  }, 1000)
}

function selectAnswer(index) {
  if (answerSelected.value) return
  selectedAnswer.value = index
  answerSelected.value = true
  clearInterval(countdown)
  setTimeout(goToNextQuestion, 5000)
}

function showCorrectAnswer() {
  answerSelected.value = true
  setTimeout(goToNextQuestion, 5000)
}

function goToNextQuestion() {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    currentQuestionIndex.value++
    currentQuestion.value = questions.value[currentQuestionIndex.value]
    selectedAnswer.value = null
    answerSelected.value = false
    timer.value = 60
    startTimer()
  } else {
    window.location.reload()
  }
}

</script>

<style scoped>
.question-screen {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  min-height: 100vh;
  padding: 30px;
  background: #f5f5f5;
  position: relative;
}

.top-bar {
  width: 100%;
  display: flex;
  justify-content: space-between;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.question-progress {
  margin-left: 10px;
}

.timer {
  margin-right: 10px;
}

.question-intitule {
  font-size: 32px;
  margin: 20px 0;
  text-align: center;
  color: #333;
}

.answers-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  width: 100%;
  max-width: 500px;
}

.answer {
  font-size: 20px;
  padding: 20px;
  background-color: #fff;
  border: 2px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.answer:hover {
  background-color: #f0f0f0;
}

.correct {
  background-color: #4caf50;
}

.wrong {
  background-color: #f44336;
}
</style>
