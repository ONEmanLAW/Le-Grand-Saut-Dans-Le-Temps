<template>
  <div id="app">
    <!-- Écran d'accueil -->
    <StartScreen v-if="screen === 'start'" @start="handleStart" />

    <!-- Écran d'attente (pour badge) -->
    <WaitingScreen v-if="screen === 'waiting'" />

    <!-- Écrans de bienvenue personnalisés -->
    <Welcome70 v-if="screen === 'welcome70'" />
    <Welcome80 v-if="screen === 'welcome80'" />

    <!-- Écran vidéo -->
    <VideoScreen v-if="screen === 'video'" ref="videoScreen" @ended="handleVideoEnded" />

    <!-- Écran de sélection du nombre de questions -->
    <QuestionCountScreen v-if="screen === 'questionCount'" @selected="handleQuestionCount" />

    <!-- Écran de sélection du thème -->
    <ThemeChoiceScreen v-if="screen === 'themeChoice'" @themeSelected="handleThemeSelected" />

    <!-- Écran de questions -->
    <QuestionScreen 
      v-if="screen === 'question'"
      :selectedTheme="selectedTheme" 
      :selectedQuestionCount="selectedQuestionCount" 
      :selectedEra="selectedEra"
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
import VideoScreen from './components/VideoScreen.vue'
import QuestionCountScreen from './components/QuestionCountScreen.vue'
import ThemeChoiceScreen from './components/ThemeChoiceScreen.vue'
import QuestionScreen from './components/QuestionScreen.vue'

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

// État
const screen = ref('start')
const videoScreen = ref(null)
const canTriggerLongScan = ref(true)
const currentRFID = ref(null)

const selectedQuestionCount = ref(null)
const selectedTheme = ref(null)
const selectedEra = ref('70')  // Valeur par défaut pour selectedEra

// WebSocket
const ws = new WebSocket('ws://192.168.1.96:8080') // ← Remplace si besoin

onMounted(() => {
  ws.onopen = () => {
    ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
  }

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)

    // ✅ Vérifie que message.data est une string avant de faire startsWith
    if (typeof message.data === 'string' && message.data.startsWith('LONG_SCAN_OK_') && canTriggerLongScan.value) {
      canTriggerLongScan.value = false

      const rfidId = message.data.replace('LONG_SCAN_OK_', '')
      currentRFID.value = rfidId

      stopAllMusic()
      welcomeMusic.play()

      if (rfidId === 'RFID_1') screen.value = 'welcome70'
      else if (rfidId === 'RFID_2') screen.value = 'welcome80'
      else screen.value = 'waiting' // fallback

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

// 🎬 Bouton démarrer
function handleStart() {
  screen.value = 'waiting'
  canTriggerLongScan.value = true
  ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
  waitingMusic.play()
}

// 🎥 Fin vidéo
function handleVideoEnded() {
  videoMusic.pause()
  videoMusic.currentTime = 0
  welcomeMusic.muted = false
  screen.value = 'questionCount'
}

// 🔢 Choix du nombre de questions
function handleQuestionCount(count) {
  selectedQuestionCount.value = count
  screen.value = 'themeChoice'
}

// 🎯 Thème choisi
function handleThemeSelected(theme) {
  selectedTheme.value = theme
  console.log(`✅ Thème choisi : ${theme}`)
  stopAllMusic()
  screen.value = 'question'
  questionMusic.play()
}

// ♻️ Réinitialisation complète
function resetInterface() {
  stopAllMusic()
  questionMusic.pause()
  questionMusic.currentTime = 0
  screen.value = 'waiting'
  videoScreen.value?.reset()
  welcomeMusic.muted = false
  waitingMusic.play()
  canTriggerLongScan.value = true
}

// 🔇 Stop toute musique
function stopAllMusic() {
  for (const music of [waitingMusic, welcomeMusic, videoMusic, backgroundMusic, questionMusic]) {
    music.pause()
    music.currentTime = 0
  }
}

// 🎵 Musique de fond selon écran
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
