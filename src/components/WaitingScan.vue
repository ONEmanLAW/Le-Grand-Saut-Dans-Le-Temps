<template>
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
</style>
