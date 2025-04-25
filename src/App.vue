<template>
  <div id="app">
    <StartScreen v-if="screen === 'start'" @start="handleStart" />
    <WaitingScreen v-if="screen === 'waiting'" />
    <WelcomeScreen v-if="screen === 'welcome'" />
    <VideoScreen v-if="screen === 'video'" ref="videoScreen" @ended="handleVideoEnded" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StartScreen from './components/StartScreen.vue'
import WaitingScreen from './components/WaitingScreen.vue'
import WelcomeScreen from './components/WelcomeScreen.vue'
import VideoScreen from './components/VideoScreen.vue'

// État général
const screen = ref('start')
const videoScreen = ref(null)
const canTriggerLongScan = ref(true) // 🔐 anti-spam

// Audio
const waitingMusic = new Audio('/sounds/1.wav')
waitingMusic.loop = true

const welcomeMusic = new Audio('/sounds/2.wav')
welcomeMusic.loop = true

const videoMusic = new Audio('/sounds/3.mp3')
videoMusic.loop = true

// WebSocket
const ws = new WebSocket('ws://192.168.1.96:8080')

onMounted(() => {
  ws.onopen = () => {
    ws.send(JSON.stringify({ client_name: 'browser', target: 'esp32' }))
  }

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)

    if (message.data === 'LONG_SCAN_OK' && canTriggerLongScan.value) {
      canTriggerLongScan.value = false // ❌ ne pas re-trigger tant que pas reset

      waitingMusic.pause()
      waitingMusic.currentTime = 0
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

// ✅ Start button
function handleStart() {
  screen.value = 'waiting'
  canTriggerLongScan.value = true // autoriser le scan
  ws.send(JSON.stringify({ client_name: 'browser', target: 'esp32' }))
  waitingMusic.play()
}

// ✅ Fin de vidéo
function handleVideoEnded() {
  videoMusic.pause()
  videoMusic.currentTime = 0
  welcomeMusic.muted = false
}

// ✅ Remet tout à zéro
function resetInterface() {
  screen.value = 'waiting'
  videoScreen.value?.reset()
  videoMusic.pause()
  videoMusic.currentTime = 0

  welcomeMusic.pause()
  welcomeMusic.currentTime = 0
  welcomeMusic.muted = false

  waitingMusic.play()
  canTriggerLongScan.value = true // ✅ on réautorise le prochain LONG_SCAN_OK
}
</script>
