<template>
  <div class="waiting-scan-container" @click="handleClickDebug">
    <!-- Musique de fond -->
    <audio ref="bgMusic" autoplay loop>
      <source src="/audio/background.mp3" type="audio/mpeg" />
      Votre navigateur ne supporte pas l'audio HTML5.
    </audio>

    <div class="title-wrapper">
      <h1 class="title pulse">Poser le badge sur l’époque</h1>
      <h1 class="subtitle pulse">de votre choix !</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WaitingScan',
  props: {
    nextStep: Function
  },
  inject: ['ws'],
  data() {
    return {
      canTriggerLongScan: true,
      clickCount: 0,
      clickTimer: null
    }
  },
  mounted() {
    this.playMusic()

    if (this.ws) {
      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        if (
          typeof message.data === 'string' &&
          message.data.startsWith('LONG_SCAN_OK_') &&
          this.canTriggerLongScan
        ) {
          this.handleScan(message.data.replace('LONG_SCAN_OK_', ''))
        }
      }
    }
  },
  beforeUnmount() {
    clearTimeout(this.clickTimer)
  },
  methods: {
    playMusic() {
      const audio = this.$refs.bgMusic
      if (audio && audio.paused) {
        audio.play().catch(() => {
          // Échec silencieux si bloqué par navigateur
        })
      }
    },

    handleScan(rfidId) {
      if (!this.canTriggerLongScan) return

      this.canTriggerLongScan = false
      const era = rfidId === 'RFID_1' || rfidId === '50' ? '50' :
                  rfidId === 'RFID_2' || rfidId === '80' ? '80' : ''

      if (era) {
        localStorage.setItem('selectedEra', era)
        this.$emit('era-selected', era)
        this.nextStep()
      } else {
        console.warn('🟡 RFID ID non reconnu :', rfidId)
        this.canTriggerLongScan = true
      }
    },

    handleClickDebug() {
      this.clickCount++
      clearTimeout(this.clickTimer)

      this.clickTimer = setTimeout(() => {
        if (this.clickCount === 3) {
          console.log('🧪 Mode debug activé (3 clics) : année 50')
          this.handleScan('50')
        } else if (this.clickCount === 4) {
          console.log('🧪 Mode debug activé (4 clics) : année 80')
          this.handleScan('80')
        }
        this.clickCount = 0
      }, 400)
    }
  }
}
</script>

<style scoped>
.waiting-scan-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  user-select: none;
  text-align: center;
  padding: 20px;
}

.title-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

.title,
.subtitle {
  font-size: 52px;
  font-weight: bold;
  color: #330006;
  text-transform: uppercase;
  margin: 0;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.2;
  }
}

.pulse {
  animation: pulse 2.5s ease-in-out infinite;
}
</style>
