<template>
  
</template>

<script>
export default {
  name: 'WebSocketClient',
  data() {
    return {
      ws: null,
      
      wsUrl: 'ws://ip:port'
    }
  },
  methods: {
    connectWebSocket() {
      this.ws = new WebSocket(this.wsUrl)

      this.$.appContext.provides.ws = this.ws

      this.ws.onopen = () => {
        console.log('✅ WebSocket connecté')
        this.ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
      }

      this.ws.onmessage = (event) => {
        console.log('📨 Message reçu :', event.data)

      }

      this.ws.onerror = (err) => {
        console.error('❌ Erreur WebSocket :', err)
      }

      this.ws.onclose = () => {
        console.warn('🔌 WebSocket fermé. Tentative de reconnexion dans 3s...')
        setTimeout(() => {
          this.connectWebSocket()
        }, 3000)
      }
    }
  },
  mounted() {
    this.connectWebSocket()
  },
  beforeUnmount() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.close()
    }
  }
}
</script>
