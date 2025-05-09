<template>
  <div id="app">
    <StartScreen v-if="screen === 'start'" @start="handleStart" />
    <WaitingScreen v-if="screen === 'waiting'" />

    <Welcome70 v-if="screen === 'welcome70'" />
    <Welcome80 v-if="screen === 'welcome80'" />

    <GeneriqueVideoScreen v-if="screen === 'video'" ref="videoScreen" @ended="handleVideoEnded" />
    <QuestionCountScreen v-if="screen === 'questionCount'" @selected="handleQuestionCount" />
    <EasyVideoScreen v-if="screen === 'introLevels'" ref="levelVideo" @ended="handleLevelVideoEnded" />
    <ThemeChoiceScreen v-if="screen === 'themeChoice'" @themeSelected="handleThemeSelected" />

    <!-- Vidéos intermédiaires -->
    <MediumVideoScreen v-if="screen === 'mediumVideo'" ref="mediumVideo" @ended="handleMediumVideoEnded" />
    <HardVideoScreen v-if="screen === 'hardVideo'" ref="hardVideo" @ended="handleHardVideoEnded" />
    <ExpertVideoScreen v-if="screen === 'expertVideo'" ref="expertVideo" @ended="handleExpertVideoEnded" />

    <!-- Écran de chargement -->
    <div v-if="screen === 'loadingQuestions'">Chargement des questions...</div>

    <!-- Questions -->
    <EasyQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'easy'"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />
    <MediumQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'medium'"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />
    <HardQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'hard'"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />
    <ExpertQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'expert'"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// Composants
import StartScreen from './components/StartScreen.vue'
import WaitingScreen from './components/WaitingScreen.vue'
import Welcome70 from './components/Welcome70.vue'
import Welcome80 from './components/Welcome80.vue'
import GeneriqueVideoScreen from './components/GeneriqueVideoScreen.vue'
import EasyVideoScreen from './components/EasyVideoScreen.vue'
import QuestionCountScreen from './components/QuestionCountScreen.vue'
import ThemeChoiceScreen from './components/ThemeChoiceScreen.vue'
import EasyQuestionScreen from './components/EasyQuestionScreen.vue'
import MediumQuestionScreen from './components/MediumQuestionScreen.vue'
import HardQuestionScreen from './components/HardQuestionScreen.vue'
import ExpertQuestionScreen from './components/ExpertQuestionScreen.vue'
import MediumVideoScreen from './components/MediumVideoScreen.vue'
import HardVideoScreen from './components/HardVideoScreen.vue'
import ExpertVideoScreen from './components/ExpertVideoScreen.vue'

// Musiques
const waitingMusic = new Audio('/sounds/1.wav')
waitingMusic.loop = true
const welcomeMusic = new Audio('/sounds/2.wav')
welcomeMusic.loop = false
const videoMusic = new Audio('/sounds/3.mp3')
videoMusic.loop = true
const backgroundMusic = new Audio('/sounds/4.wav')
backgroundMusic.loop = true
const questionMusic = new Audio('/sounds/5.mp3')
questionMusic.loop = true
const levelMusic = new Audio('/sounds/6.mp3')
levelMusic.loop = true

// États
const screen = ref('start')
const selectedQuestionCount = ref(null)
const selectedQuestionsPerLevel = ref(0)
const selectedTheme = ref(null)
const selectedEra = ref('70')
const selectedDifficulty = ref('easy')
const selectedQuestions = ref([])
const currentLevelIndex = ref(0)
const levelOrder = ['easy', 'medium', 'hard', 'expert']

const videoScreen = ref(null)
const levelVideo = ref(null)
const mediumVideo = ref(null)
const hardVideo = ref(null)
const expertVideo = ref(null)

const canTriggerLongScan = ref(true)
const currentRFID = ref(null)

// WebSocket
const ws = new WebSocket('ws://192.168.1.96:8080')

onMounted(() => {
  ws.onopen = () => {
    ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
  }

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)

    if (typeof message.data === 'string' && message.data.startsWith('LONG_SCAN_OK_') && canTriggerLongScan.value) {
      canTriggerLongScan.value = false
      const rfidId = message.data.replace('LONG_SCAN_OK_', '')
      currentRFID.value = rfidId

      stopAllMusic()
      welcomeMusic.play()

      if (rfidId === 'RFID_1') {
        screen.value = 'welcome70'
        selectedEra.value = '70'
      } else if (rfidId === 'RFID_2') {
        screen.value = 'welcome80'
        selectedEra.value = '80'
      } else {
        screen.value = 'waiting'
      }

      setTimeout(() => {
        screen.value = 'video'
        videoScreen.value?.play()
        welcomeMusic.muted = true
        videoMusic.play()
      }, 5000)
    }

    if (message.data === 'WAIT_FOR_BADGE') {
      screen.value = 'waiting'
      if (waitingMusic.paused) waitingMusic.play()
    }

    if (typeof message.data === 'string' && message.data.startsWith('BADGE_REMOVED_')) {
      resetInterface()
    }
  }
})

function handleStart() {
  screen.value = 'waiting'
  canTriggerLongScan.value = true
  ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
  waitingMusic.play()
}

function handleVideoEnded() {
  videoMusic.pause()
  videoMusic.currentTime = 0
  welcomeMusic.muted = false
  screen.value = 'questionCount'
}

function handleQuestionCount(count) {
  selectedQuestionCount.value = count
  selectedQuestionsPerLevel.value = Math.floor(count / 4)
  stopAllMusic()
  screen.value = 'introLevels'
  levelMusic.play()
}

function handleLevelVideoEnded() {
  levelMusic.pause()
  screen.value = 'themeChoice'
}

async function handleThemeSelected(theme) {
  selectedTheme.value = theme
  stopAllMusic()
  screen.value = 'loadingQuestions'

  const era = selectedEra.value
  const filePath = `/data/questions_${era}.json`

  try {
    const response = await fetch(filePath)
    const allQuestions = await response.json()

    const levelMap = {
      easy: 'facile',
      medium: 'moyen',
      hard: 'difficile',
      expert: 'expert'
    }

    const themeQuestions = allQuestions[theme]
    if (!themeQuestions) throw new Error("Thème non trouvé dans les données.")

    const difficultyQuestions = themeQuestions[levelMap[selectedDifficulty.value]]
    if (!difficultyQuestions) throw new Error("Niveau non trouvé pour ce thème.")

    const selected = difficultyQuestions.slice(0, selectedQuestionsPerLevel.value)

    if (selected.length === 0) {
      alert("Aucune question disponible pour ce thème et niveau.")
      screen.value = 'themeChoice'
      return
    }

    selectedQuestions.value = selected

    if (selectedDifficulty.value === 'easy') {
      screen.value = 'question'
      questionMusic.play()
    } else {
      screen.value = `${selectedDifficulty.value}Video`
      setTimeout(() => {
        getVideoRef().value?.play()
      }, 100)
    }
  } catch (err) {
    console.error("Erreur lors du chargement des questions :", err)
    alert("Erreur de chargement.")
    screen.value = 'themeChoice'
  }
}

function handleLevelCompleted() {
  currentLevelIndex.value++

  if (currentLevelIndex.value >= levelOrder.length) {
    screen.value = 'waiting'
    return
  }

  selectedDifficulty.value = levelOrder[currentLevelIndex.value]
  screen.value = `${selectedDifficulty.value}Video`
  setTimeout(() => {
    getVideoRef().value?.play()
  }, 100)
}

function handleMediumVideoEnded() {
  screen.value = 'loadingQuestions'
  loadQuestionsForDifficulty('medium') // On charge les questions medium
}

function handleHardVideoEnded() {
  screen.value = 'loadingQuestions'
  loadQuestionsForDifficulty('hard') // On charge les questions hard
}

function handleExpertVideoEnded() {
  screen.value = 'loadingQuestions'
  loadQuestionsForDifficulty('expert') // On charge les questions expert
}

async function loadQuestionsForDifficulty(difficulty) {
  try {
    const era = selectedEra.value
    const filePath = `/data/questions_${era}.json`
    const response = await fetch(filePath)
    const allQuestions = await response.json()

    const levelMap = {
      easy: 'facile',
      medium: 'moyen',
      hard: 'difficile',
      expert: 'expert'
    }

    const themeQuestions = allQuestions[selectedTheme.value]
    const difficultyQuestions = themeQuestions[levelMap[difficulty]] // On utilise le niveau dynamique ici

    const selected = difficultyQuestions.slice(0, selectedQuestionsPerLevel.value)

    if (selected.length === 0) {
      alert("Aucune question disponible pour ce thème et niveau.")
      screen.value = 'themeChoice'
      return
    }

    selectedQuestions.value = selected

    screen.value = 'question'  // Affiche l'écran des questions
    questionMusic.play()

  } catch (err) {
    console.error("Erreur lors du chargement des questions :", err)
    alert("Erreur de chargement.")
    screen.value = 'themeChoice'
  }
}

function resetInterface() {
  stopAllMusic()
  questionMusic.pause()
  questionMusic.currentTime = 0
  screen.value = 'waiting'
  videoScreen.value?.reset()
  welcomeMusic.muted = false
  waitingMusic.play()
  canTriggerLongScan.value = true
  currentLevelIndex.value = 0
  selectedDifficulty.value = 'easy'
}

function stopAllMusic() {
  for (const music of [waitingMusic, welcomeMusic, videoMusic, backgroundMusic, questionMusic, levelMusic]) {
    music.pause()
    music.currentTime = 0
  }
}

function getVideoRef() {
  switch (selectedDifficulty.value) {
    case 'medium': return mediumVideo
    case 'hard': return hardVideo
    case 'expert': return expertVideo
    default: return null
  }
}

watch(screen, (newScreen) => {
  if (newScreen === 'questionCount' || newScreen === 'themeChoice') {
    if (backgroundMusic.paused) backgroundMusic.play()
  } else {
    if (backgroundMusic.currentTime === backgroundMusic.duration) {
      backgroundMusic.currentTime = 0
    }
  }
})
</script>

<style>
#app {
  font-family: Arial, sans-serif;
}
</style>
