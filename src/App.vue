<template>
  <div id="app">
    <StartScreen v-if="screen === 'start'" @start="handleStart" />
    <WaitingScreen v-if="screen === 'waiting'" />
    <WelcomeScreen v-if="screen === 'welcome'" />
    <VideoScreen v-if="screen === 'video'" ref="videoScreen" @ended="handleVideoEnded" />
    <QuestionCountScreen v-if="screen === 'questionCount'" @selected="handleQuestionCount" />
    <ThemeChoiceScreen v-if="screen === 'themeChoice'" @themeSelected="handleThemeSelected" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import StartScreen from './components/StartScreen.vue'
import WaitingScreen from './components/WaitingScreen.vue'
import WelcomeScreen from './components/WelcomeScreen.vue'
import VideoScreen from './components/VideoScreen.vue'
import QuestionCountScreen from './components/QuestionCountScreen.vue'
import ThemeChoiceScreen from './components/ThemeChoiceScreen.vue'

// ⏺️ Musiques
const waitingMusic = new Audio('/sounds/1.wav')
waitingMusic.loop = true

const welcomeMusic = new Audio('/sounds/2.wav')
welcomeMusic.loop = false

const videoMusic = new Audio('/sounds/3.mp3')
videoMusic.loop = true

const backgroundMusic = new Audio('/sounds/4.wav') // 🎶 musique pour les choix
backgroundMusic.loop = true

// État
const screen = ref('start')
const videoScreen = ref(null)
const canTriggerLongScan = ref(true)

const selectedQuestionCount = ref(null)
const selectedTheme = ref(null)

const ws = new WebSocket('ws://192.168.1.96:8080')

// 📡 WebSocket setup
onMounted(() => {
  ws.onopen = () => {
    ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
  }

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)

    if (message.data === 'LONG_SCAN_OK' && canTriggerLongScan.value) {
      canTriggerLongScan.value = false

      stopAllMusic()
      welcomeMusic.play()

      screen.value = 'welcome'

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

    if (message.data === 'BADGE_REMOVED') {
      resetInterface()
    }
  }
})

// 🎬 Start button
function handleStart() {
  screen.value = 'waiting'
  canTriggerLongScan.value = true
  ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
  waitingMusic.play()
}

// 📽️ Fin vidéo → choix nombre de questions
function handleVideoEnded() {
  videoMusic.pause()
  videoMusic.currentTime = 0
  welcomeMusic.muted = false
  screen.value = 'questionCount'
}

// 🔢 Choix nombre questions → choix thème
function handleQuestionCount(count) {
  selectedQuestionCount.value = count
  screen.value = 'themeChoice'
}

// 🎯 Thème choisi → prêt pour la suite
function handleThemeSelected(theme) {
  selectedTheme.value = theme
  console.log(`✅ Thème choisi : ${theme}`)

  stopAllMusic()
  // → continue logique ici (écran quiz par ex)
}

// 🧹 Reset complet
function resetInterface() {
  stopAllMusic()
  screen.value = 'waiting'
  videoScreen.value?.reset()
  welcomeMusic.muted = false
  waitingMusic.play()
  canTriggerLongScan.value = true
}

// 🔇 Stop toutes les musiques
function stopAllMusic() {
  for (const music of [waitingMusic, welcomeMusic, videoMusic, backgroundMusic]) {
    music.pause()
    music.currentTime = 0
  }
}

// 🎵 Réagit quand l'écran change
watch(screen, (newScreen) => {
  // Si on arrive sur questionCount ou themeChoice, on démarre la musique de fond
  if (newScreen === 'questionCount' || newScreen === 'themeChoice') {
    if (backgroundMusic.paused) {
      backgroundMusic.play()
    }
  } 
  // Sinon, on arrête la musique de fond seulement si on sort de ces écrans
  else if (newScreen !== 'waiting' && newScreen !== 'start') {
    // On arrête la musique de fond dès qu'on quitte les écrans de choix (questionCount, themeChoice)
    backgroundMusic.pause()
    backgroundMusic.currentTime = 0
  }
})
</script>
