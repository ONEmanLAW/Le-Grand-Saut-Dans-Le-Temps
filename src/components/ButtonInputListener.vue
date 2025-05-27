<template>
  <div style="display: none;"></div>
</template>

<script>
export default {
  name: "ButtonInputListener",
  props: {
    onButtonPress: {
      type: Function,
      required: true
    },
    active: {
      type: Boolean,
      default: false
    }
  },
  inject: ['ws'],
  mounted() {
    if (this.ws) {
      this.ws.onmessage = (event) => {
        if (!this.active) return

        try {
          const message = JSON.parse(event.data)
          if (message?.data && ['A', 'B', 'C', 'D'].includes(message.data)) {
            this.onButtonPress(message.data)
          }
        } catch (err) {
          console.warn("❌ Message WebSocket invalide", err)
        }
      }
    }
  }
}
</script>

