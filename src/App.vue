<template>
  <div @touchstart.passive="handleTouch" class="app-container">
    <WebSocketClient />
    <component
      v-if="currentStep"
      :is="currentStep.objectId"
      v-bind="currentStep.props"
      :next-step="nextStep"
    />
  </div>
</template>

<script>
import WebSocketClient from './components/WebSocketClient.vue'
import StartScreen from './components/StartScreen.vue'
import GenericScreen from './components/GenericScreen.vue'
import WaitingScan from './components/WaitingScan.vue'
import EraVideoScreen from './components/EraVideoScreen.vue'
import GameRulesIntro from './components/GameRulesIntro.vue'
import QuestionCount from './components/QuestionCount.vue'

export default {
  name: 'App',
  components: {
    WebSocketClient,
    StartScreen,
    GenericScreen,
    WaitingScan,
    EraVideoScreen,
    GameRulesIntro,
    QuestionCount
  },
  data() {
    return {
      flow: [],
      currentIndex: 0,
      tapCount: 0,
      tapTimer: null,
    }
  },
  computed: {
    currentStep() {
      return this.flow[this.currentIndex] || null
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
    }
  },
  mounted() {
    this.loadFlow()
  }
}
</script>
