<script>
export default {
  name: 'WebSocketClient',
  data() {
    return {
      ws: null,
      //wsUrl: 'ws://172.28.59.61:8080' // IP École
      wsUrl: 'ws://192.168.254.50:8080' // IP Partage
    }
  },
  methods: {
    connectWebSocket() {
      this.ws = new WebSocket(this.wsUrl)

      this.ws.onopen = () => {
        console.log('✅ WebSocket connecté')
        this.ws.send(JSON.stringify({ client_name: 'browser', target: 'raspberry' }))
      }

      this.ws.onmessage = (event) => {
        console.log('📨 Message reçu :', event.data)

        // Ajoute ici tes actions plus tard si besoin
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
