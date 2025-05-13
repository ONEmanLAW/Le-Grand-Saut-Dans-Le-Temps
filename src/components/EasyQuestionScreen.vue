<template>
  <div class="question-screen">
    <!-- ÉCRAN INTRO MUSIQUE -->
    <div v-if="showMusicIntro && currentQuestion.beforeMusic">
      <div class="top-bar">
        <div class="question-progress">Question : {{ currentQuestionIndex + 1 }}/{{ questions.length }}</div>
      </div>
      <div class="music-intro-screen">
        <h2>🎵 Écoutez la musique 🎵</h2>
        <button @click="startMusicIntro" class="play-button" :disabled="audioPlayed">▶️ Lancer l'extrait</button>
      </div>
    </div>

    <!-- ÉCRAN QUESTION -->
    <div v-else-if="!showFeedback">
      <div class="top-bar">
        <div class="question-progress">Question : {{ currentQuestionIndex + 1 }}/{{ questions.length }}</div>
      </div>

      <div class="question-intitule">{{ currentQuestion.question }}</div>

      <div class="answers-grid">
        <button
          v-for="(answer, index) in currentQuestion.answers"
          :key="index"
          :class="[
            'answer',
            answerSelected && index === currentQuestion.correctIndex ? 'correct' : '',
            selectedAnswer === index && index !== currentQuestion.correctIndex ? 'wrong' : '',
            answerSelected && index !== selectedAnswer && index !== currentQuestion.correctIndex ? 'fade-out' : '',
            index === 0 ? 'red' : index === 1 ? 'blue' : index === 2 ? 'yellow' : 'green'
          ]"
          @click="selectAnswer(index)"
          :disabled="answerSelected"
        >
          {{ answer }}
        </button>
      </div>
    </div>

    <!-- ÉCRAN FEEDBACK -->
    <div v-else class="feedback-screen">
      <div class="top-bar">
        <div class="question-progress">Question : {{ currentQuestionIndex + 1 }}/{{ questions.length }}</div>
      </div>
      <div class="feedback-content">
        <img
          :src="`/images/${currentQuestion.feedback.image}`"
          class="feedback-image"
          alt="Feedback"
        />
        <div class="feedback-text">{{ currentQuestion.feedback.text }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  questions: { type: Array, required: true }
})
const emit = defineEmits(['finished'])

const currentQuestionIndex = ref(0)
const currentQuestion = ref(props.questions[0])
const selectedAnswer = ref(null)
const answerSelected = ref(false)
const score = ref(0)
const showFeedback = ref(false)
const showMusicIntro = ref(!!currentQuestion.value.beforeMusic)
const audioPlayed = ref(false)

let beforeAudio = null
let afterAudio = null

function startMusicIntro() {
  if (audioPlayed.value) return // ❌ empêcher plusieurs clics
  audioPlayed.value = true // ✅ bloque le bouton

  // Lecture de la musique
  beforeAudio = new Audio(currentQuestion.value.beforeMusic)
  beforeAudio.play()

  // Passage à la question après 20 secondes FIXES
  setTimeout(() => {
    showMusicIntro.value = false
  }, 20000)
}

function selectAnswer(index) {
  if (answerSelected.value) return
  selectedAnswer.value = index
  answerSelected.value = true

  if (index === currentQuestion.value.correctIndex) {
    score.value++
  }

  setTimeout(() => {
    showFeedback.value = true

    if (currentQuestion.value.afterMusic) {
      afterAudio = new Audio(currentQuestion.value.afterMusic)
      afterAudio.play()
    }

    setTimeout(() => {
      showFeedback.value = false
      moveToNextQuestion()
    }, 15000)
  }, 5000)
}

function moveToNextQuestion() {
  if (currentQuestionIndex.value + 1 < props.questions.length) {
    currentQuestionIndex.value++
    currentQuestion.value = props.questions[currentQuestionIndex.value]
    selectedAnswer.value = null
    answerSelected.value = false
    showFeedback.value = false
    showMusicIntro.value = !!currentQuestion.value.beforeMusic
    audioPlayed.value = false
  } else {
    emit('finished', score.value)
  }
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
  color: black;
}
.top-bar {
  font-size: 18px;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.question-progress {
  font-weight: bold;
  color: black;
  border: 2px solid black;
  border-radius: 10px;
  background-color: white;
  padding: 30px 45px;
  margin-top: 40px;
  font-size: 52px;
}
.question-intitule {
  font-size: 48px;
  margin-bottom: 40px;
  padding: 0 75px;
  font-weight: bold;
}
.answers-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 50px;
  margin-top: 20px;
  padding: 0 50px;
}
.answer {
  color: white;
  font-weight: 800;
  font-size: 38px;
  padding: 30px 30px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s, transform 1s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}
.red { background-color: red; }
.blue { background-color: blue; }
.yellow { background-color: #C89214; }
.green { background-color: green; }
.correct { background-color: #4caf50; }
.wrong { background-color: #f44336; }
.fade-out {
  opacity: 0;
  transform: scale(0.9);
  pointer-events: none;
}
.music-intro-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh;
}
.play-button {
  margin-top: 30px;
  padding: 20px 40px;
  font-size: 32px;
  border-radius: 20px;
  border: none;
  background-color: #007BFF;
  color: white;
  cursor: pointer;
}
.play-button:disabled {
  background-color: #999;
  cursor: not-allowed;
}
.feedback-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.feedback-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.feedback-image {
  max-width: 600px;
  margin-bottom: 20px;
}
.feedback-text {
  font-size: 38px;
  font-weight: bold;
  max-width: 80%;
  padding: 0 20px;
}
</style>
