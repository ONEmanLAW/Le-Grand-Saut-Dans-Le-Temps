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
    <h1>Poser le badge sur l'époque de votre choix !</h1>
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
      debugInput: '',
      clickCount: 0,
      clickTimer: null
    }
  },
  mounted() {
    // Écoute WebSocket
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

    // Mode debug clavier
    window.addEventListener('keydown', this.handleKeydown)
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeydown)
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
    handleKeydown(e) {
      this.debugInput += e.key
      if (this.debugInput.length >= 2) {
        const value = this.debugInput.slice(-2)
        if (value === '50' || value === '80') {
          console.log(`🧪 Mode debug activé (clavier) : scan simulé pour ${value}`)
          this.handleScan(value)
        }
        this.debugInput = ''
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
      }, 400) // 400ms pour taper rapidement
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
</style>

