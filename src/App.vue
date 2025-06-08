<template>
  <!-- Ajout d'une classe dynamique selon l'époque -->
  <div
    @touchstart.passive="handleTouch"
    :class="['app-container', backgroundEraClass]"
  >
    <WebSocketClient />
    <component
      v-if="currentStep"
      :is="currentStep.objectId"
      v-bind="currentStep.props"
      :next-step="nextStep"
      @era-selected="onEraSelected"
    />
  </div>
</template>

<script>
import WebSocketClient from './components/WebSocketClient.vue'
import ButtonInputListener from './components/ButtonInputListener.vue'
import StartScreen from './components/StartScreen.vue'
import GenericScreen from './components/GenericScreen.vue'
import WaitingScan from './components/WaitingScan.vue'
import EraVideoScreen from './components/EraVideoScreen.vue'
import GameRulesIntro from './components/GameRulesIntro.vue'
import QuestionCount from './components/QuestionCount.vue'
import ThemeCount from './components/ThemeCount.vue'
import ThemeIntroVideo from './components/ThemeIntroVideo.vue'
import QuestionScreen from './components/QuestionScreen.vue'
import TropheeVideo from './components/TropheeVideo.vue'
import EndGameScreen from './components/EndGameScreen.vue'

export default {
  name: 'App',
  components: {
    WebSocketClient,
    ButtonInputListener,
    StartScreen,
    GenericScreen,
    WaitingScan,
    EraVideoScreen,
    GameRulesIntro,
    QuestionCount,
    ThemeCount,
    ThemeIntroVideo,
    QuestionScreen,
    TropheeVideo,
    EndGameScreen
  },
  data() {
    return {
      flow: [],
      currentIndex: 0,
      tapCount: 0,
      tapTimer: null,
      selectedEra: null,  // Pas d'époque choisie au départ
    }
  },
  computed: {
    currentStep() {
      return this.flow[this.currentIndex] || null
    },
    backgroundEraClass() {
      console.log('selectedEra:', this.selectedEra)
      if (this.selectedEra === '50') return 'bg-era-50'
      if (this.selectedEra === '80') return 'bg-era-80'
      return 'bg-default'
    }
  },
  methods: {
    nextStep() {
      if (this.currentIndex < this.flow.length - 1) {
        this.currentIndex++
      } else {
        console.log('Fin du flow')
      }
    },
    async loadFlow() {
      try {
        const res = await fetch('/data/flow.json')
        const data = await res.json()
        this.flow = data
      } catch (e) {
        console.error('Erreur de chargement de flow.json', e)
      }
    },
    handleTouch() {
      this.tapCount++
      if (this.tapTimer) clearTimeout(this.tapTimer)

      this.tapTimer = setTimeout(() => {
        if (this.tapCount >= 5) {
          window.location.reload()
        }
        this.tapCount = 0
      }, 500)
    },
    onEraSelected(era) {
      // Ne change le fond que si l'utilisateur a fait un vrai choix (ignore '50' par défaut sans localStorage)
      if (era === '50' && !localStorage.getItem('selectedEra')) {
        // Ignore cette valeur par défaut automatique
        return
      }
      this.selectedEra = era
      localStorage.setItem('selectedEra', era)
    }
  },
  mounted() {
    this.loadFlow()
    // Ne pas précharger selectedEra depuis localStorage pour éviter le changement automatique
    // this.selectedEra = localStorage.getItem('selectedEra') || null
  }
}
</script>

<style>
.app-container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: #FFAE59;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  transition: background-image 0.5s ease-in-out;
}

/* Classes pour fond selon époque */
.bg-default {
  background-color: #FFAE59;
}
.bg-era-50 {
  background-image: url('/images/era50.png');
}
.bg-era-80 {
  background-image: url('/images/era80.png');
}
</style>
