<template>
  <div class="question-screen">
    <div class="top-bar">
      <div class="question-progress">{{ currentQuestionIndex + 1 }}/{{ totalQuestions }}</div>
      <!-- Afficher le timer uniquement si la difficulté est "expert" -->
      <div class="timer" v-if="difficulty === 'expert'">{{ timer }}s</div>
    </div>

    <component
      :is="currentDifficultyComponent"
      :questions="questions"
      :currentQuestion="currentQuestion"
      :currentQuestionIndex="currentQuestionIndex"
      :totalQuestions="totalQuestions"
      :timer="timer"
      :selectedAnswer="selectedAnswer"
      :answerSelected="answerSelected"
      @selectAnswer="selectAnswer"
      @goToNextQuestion="goToNextQuestion"
      @showCorrectAnswer="showCorrectAnswer"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import EasyQuestionScreen from './EasyQuestionScreen.vue'
import MediumQuestionScreen from './MediumQuestionScreen.vue'
import HardQuestionScreen from './HardQuestionScreen.vue'
import ExpertQuestionScreen from './ExpertQuestionScreen.vue'

// Props
const props = defineProps({
  selectedTheme: { type: String, required: true },
  selectedQuestionCount: { type: Number, required: true },
  selectedEra: { type: String, required: true },
  difficulty: { type: String, required: true }  // "easy", "medium", "hard", "expert"
})

const questions = ref([])
const currentQuestion = ref({})
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const answerSelected = ref(false)
const timer = ref(60)
const totalQuestions = ref(0)
let countdown = null

// Choix du composant basé sur la difficulté
const currentDifficultyComponent = ref(EasyQuestionScreen) // Valeur par défaut

// Watch pour la difficulté, change le composant à afficher
watch(() => props.difficulty, (newDifficulty) => {
  switch (newDifficulty) {
    case 'easy':
      currentDifficultyComponent.value = EasyQuestionScreen
      break
    case 'medium':
      currentDifficultyComponent.value = MediumQuestionScreen
      break
    case 'hard':
      currentDifficultyComponent.value = HardQuestionScreen
      break
    case 'expert':
      currentDifficultyComponent.value = ExpertQuestionScreen
      break
  }
  // Si la difficulté est expert, démarrer le timer
  if (newDifficulty === 'expert') {
    startTimer()
  } else {
    clearInterval(countdown) // Si la difficulté n'est pas expert, arrêter le timer
    timer.value = 0
  }
})

onMounted(async () => {
  await loadQuestions()
})

async function loadQuestions() {
  try {
    // Charger les questions pour l'époque et le thème
    const res = await fetch(`/data/questions_${props.selectedEra}.json`)
    if (!res.ok) throw new Error('Erreur lors du chargement du fichier JSON')

    const data = await res.json()
    const selectedQuestions = data[props.selectedTheme] || []

    questions.value = selectedQuestions.sort(() => 0.5 - Math.random()).slice(0, props.selectedQuestionCount)
    totalQuestions.value = questions.value.length
    currentQuestion.value = questions.value[0]
  } catch (error) {
    console.error('Erreur de chargement des questions :', error)
  }
}

// Démarre le timer seulement pour la difficulté "expert"
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
  clearInterval(countdown) // Arrêter le timer après la sélection de la réponse
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
    if (props.difficulty === 'expert') startTimer() // Démarrer à nouveau le timer si c'est expert
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
</style>
