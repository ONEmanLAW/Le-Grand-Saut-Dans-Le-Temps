<template>
  <div class="start-screen" @click="handleClick">
    <h1 class="start-button">APPUYER POUR COMMENCER</h1>

    <ButtonInputListener
      :active="true"
      :onButtonPress="handleButtonPress"
    />
  </div>
</template>

<script>
import ButtonInputListener from './ButtonInputListener.vue'

export default {
  name: 'StartScreen',
  components: { ButtonInputListener },
  props: {
    nextStep: { type: Function, required: true }
  },
  methods: {
    handleClick() {
      this.nextStep()
    },
    handleButtonPress(buttonId) {
      const validButtons = ['A', 'B', 'C', 'D']
      if (validButtons.includes(buttonId)) {
        this.nextStep()
      }
    }
  }
}
</script>

<style scoped>
.start-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  background-color: #FFAE59;
  cursor: pointer;
}

.start-button {
  color: #330006;
  font-size: 64px;
  font-weight: bold;
  text-transform: uppercase;
  padding: 40px 80px;
  border: 6px solid #330006;
  border-radius: 20px;
  animation: pulse 2.5s ease-in-out infinite;
  opacity: 0;
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
</style>
