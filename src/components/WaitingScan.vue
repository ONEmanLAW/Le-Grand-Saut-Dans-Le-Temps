<!-- <template>
  <div class="waiting-scan-container">
    <p>En attente du scan du badge…</p>
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
      canTriggerLongScan: true
    }
  },
  mounted() {
    if (this.ws) {
      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        if (
          typeof message.data === 'string' &&
          message.data.startsWith('LONG_SCAN_OK_') &&
          this.canTriggerLongScan
        ) {
          this.canTriggerLongScan = false
          const rfidId = message.data.replace('LONG_SCAN_OK_', '')
          localStorage.setItem(
            'selectedEra',
            rfidId === 'RFID_1' ? '50' : rfidId === 'RFID_2' ? '80' : ''
          )
          this.nextStep()
        }
      }
    }
  }
}
</script>

<style scoped>
.waiting-scan-container {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 52px;
  font-weight: bold;
  color: black;
  height: 100vh;
  user-select: none;
}
</style> -->







<!-- Code With Debug here -->

<template>
  <div class="waiting-scan-container" @click="handleClickDebug">
    <h1 class="title pulse">Poser le badge sur l'époque de votre choix !</h1>
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
    // WebSocket listen
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

    // **Debug clavier et debug 3 clics souris automatique supprimés**
  },
  beforeUnmount() {
    clearTimeout(this.clickTimer)
  },
  methods: {
    handleScan(rfidId) {
      if (!this.canTriggerLongScan) return

      this.canTriggerLongScan = false
      const era = rfidId === 'RFID_1' || rfidId === '50' ? '50' :
                  rfidId === 'RFID_2' || rfidId === '80' ? '80' : ''

      if (era) {
        localStorage.setItem('selectedEra', era)
        this.nextStep()
      } else {
        console.warn('🟡 RFID ID non reconnu :', rfidId)
        this.canTriggerLongScan = true
      }
    },

    // Suppression de handleKeydown (debug clavier)

    handleClickDebug() {
      this.clickCount++
      clearTimeout(this.clickTimer)

      this.clickTimer = setTimeout(() => {
        // Garder le comportement normal 3 clics rapides pour "debug tactile"
        if (this.clickCount === 3) {
          console.log('🧪 Mode debug activé (3 clics) : année 50')
          this.handleScan('50')
        } else if (this.clickCount === 4) {
          console.log('🧪 Mode debug activé (4 clics) : année 80')
          this.handleScan('80')
        }
        this.clickCount = 0
      }, 400) // 400ms délai pour taper rapidement
    }
  }
}
</script>

<style scoped>
.waiting-scan-container {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 52px;
  font-weight: bold;
  color: black;
  height: 100vh;
  user-select: none;
  text-align: center;
  padding: 20px;
}

.title {
  text-transform: uppercase;
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


