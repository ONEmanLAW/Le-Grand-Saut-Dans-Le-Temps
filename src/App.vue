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

    <MediumVideoScreen v-if="screen === 'mediumVideo'" ref="mediumVideo" @ended="handleMediumVideoEnded" />
    <HardVideoScreen v-if="screen === 'hardVideo'" ref="hardVideo" @ended="handleHardVideoEnded" />
    <ExpertVideoScreen v-if="screen === 'expertVideo'" ref="expertVideo" @ended="handleExpertVideoEnded" />
    <EndVideo v-if="screen === 'endVideo'" @videoEnded="handleEndVideoFinished" />


    

    <div v-if="screen === 'loadingQuestions'">Chargement des questions...</div>

    <EasyQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'easy'"
      ref="easyQuestionRef"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />
    <MediumQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'medium'"
      ref="mediumQuestionRef"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />
    <HardQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'hard'"
      ref="hardQuestionRef"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />
    <ExpertQuestionScreen 
      v-if="screen === 'question' && selectedDifficulty === 'expert'"
      ref="expertQuestionRef"
      :questions="selectedQuestions"
      @finished="handleLevelCompleted"
    />

    

    <EndVideo v-if="screen === 'endVideo'" @videoEnded="handleEndVideoFinished" />
    <ScoreScreen 
      v-if="screen === 'score'" 
      :score="finalScore" 
      :total="selectedQuestionCount" 
      @restart="resetInterface" 
    />

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

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
import ScoreScreen from './components/ScoreScreen.vue'
import EndVideo from './components/EndVideo.vue'


const screen = ref('start')
const selectedQuestionCount = ref(null)
const selectedQuestionsPerLevel = ref(0)
const selectedTheme = ref(null)
const selectedEra = ref('70')
const selectedDifficulty = ref('easy')
const selectedQuestions = ref([])
const currentLevelIndex = ref(0)
const levelOrder = ['easy', 'medium', 'hard', 'expert']
const finalScore = ref(0) // ✅

const videoScreen = ref(null)
const levelVideo = ref(null)
const mediumVideo = ref(null)
const hardVideo = ref(null)
const expertVideo = ref(null)

const easyQuestionRef = ref(null)
const mediumQuestionRef = ref(null)
const hardQuestionRef = ref(null)
const expertQuestionRef = ref(null)

const canTriggerLongScan = ref(true)
const currentRFID = ref(null)

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
const mediumLevelMusic = new Audio('/sounds/medium.mp3')
mediumLevelMusic.loop = true
const hardLevelMusic = new Audio('/sounds/hard.mp3')
hardLevelMusic.loop = true
const expertLevelMusic = new Audio('/sounds/expert.mp3')
expertLevelMusic.loop = true

const ws = new WebSocket('ws://192.168.208.50:8080') // Partage

onMounted(() => {
  ws.onopen = () => {
    ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
  }

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)

    if (typeof message.data === 'string' && ['A', 'B', 'C', 'D'].includes(message.data)) {
      if (selectedDifficulty.value === 'easy') {
        easyQuestionRef.value?.selectAnswerFromHardware(message.data)
      } else if (selectedDifficulty.value === 'medium') {
        mediumQuestionRef.value?.selectAnswerFromHardware(message.data)
      } else if (selectedDifficulty.value === 'hard') {
        hardQuestionRef.value?.selectAnswerFromHardware(message.data)
      } else if (selectedDifficulty.value === 'expert') {
        expertQuestionRef.value?.selectAnswerFromHardware(message.data)
      }
    }

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
    if (!themeQuestions) throw new Error("Thème non trouvé.")

    const difficultyQuestions = themeQuestions[levelMap[selectedDifficulty.value]]
    if (!difficultyQuestions) throw new Error("Niveau non trouvé.")

    const selected = difficultyQuestions.slice(0, selectedQuestionsPerLevel.value)

    if (selected.length === 0) {
      alert("Aucune question trouvée.")
      screen.value = 'themeChoice'
      return
    }

    selectedQuestions.value = selected

    if (selectedDifficulty.value === 'easy') {
      screen.value = 'question'
      questionMusic.play()
    } else {
      screen.value = `${selectedDifficulty.value}Video`

      switch (selectedDifficulty.value) {
        case 'medium': mediumLevelMusic.play(); break
        case 'hard': hardLevelMusic.play(); break
        case 'expert': expertLevelMusic.play(); break
      }

      setTimeout(() => getVideoRef().value?.play(), 100)
    }
  } catch (err) {
    console.error("Erreur chargement :", err)
    alert("Erreur de chargement.")
    screen.value = 'themeChoice'
  }
}

function handleLevelCompleted(score) {
  finalScore.value += score
  currentLevelIndex.value++

  if (currentLevelIndex.value >= levelOrder.length) {
    screen.value = 'endVideo'
    questionMusic.pause()
    return
  }

  selectedDifficulty.value = levelOrder[currentLevelIndex.value]
  screen.value = `${selectedDifficulty.value}Video`

  stopAllMusic()
  switch (selectedDifficulty.value) {
    case 'medium': mediumLevelMusic.play(); break
    case 'hard': hardLevelMusic.play(); break
    case 'expert': expertLevelMusic.play(); break
  }

  setTimeout(() => getVideoRef().value?.play(), 100)
}

function handleMediumVideoEnded() {
  stopAllMusic()
  screen.value = 'loadingQuestions'
  loadQuestionsForDifficulty('medium')
}

function handleHardVideoEnded() {
  stopAllMusic()
  screen.value = 'loadingQuestions'
  loadQuestionsForDifficulty('hard')
}

function handleExpertVideoEnded() {
  stopAllMusic()
  screen.value = 'loadingQuestions'
  loadQuestionsForDifficulty('expert')
}

function handleEndVideoFinished() {
  screen.value = 'score'
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
    const difficultyQuestions = themeQuestions[levelMap[difficulty]]
    const selected = difficultyQuestions.slice(0, selectedQuestionsPerLevel.value)

    if (selected.length === 0) {
      alert("Aucune question pour ce niveau.")
      screen.value = 'themeChoice'
      return
    }

    selectedQuestions.value = selected
    screen.value = 'question'
    questionMusic.play()
  } catch (err) {
    console.error("Erreur chargement questions :", err)
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
  finalScore.value = 0
}

function stopAllMusic() {
  for (const music of [
    waitingMusic,
    welcomeMusic,
    videoMusic,
    backgroundMusic,
    questionMusic,
    levelMusic,
    mediumLevelMusic,
    hardLevelMusic,
    expertLevelMusic
  ]) {
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
  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Roboto:wght@700&display=swap');

#app {
  font-family: 'Open Sans', sans-serif;
  background-color: #FFC800;
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 52px;
  margin: 20px 0;
}
h2 {
  font-family: 'Open Sans', sans-serif;
  font-size: 48px;
  margin: 18px 0;
}
h3 {
  font-family: 'Open Sans', sans-serif;
  font-size: 36px;
  margin: 16px 0;
}
p {
  font-family: 'Open Sans', sans-serif;
  font-size: 18px;
  line-height: 1.6;
  margin: 12px 0;
}
</style>
