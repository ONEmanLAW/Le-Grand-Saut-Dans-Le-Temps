<template>
  <div class="start-screen" @click="handleClick">
    <!-- Musique de fond -->
    <audio ref="bgMusic" autoplay loop>
      <source src="/audio/background.mp3" type="audio/mpeg" />
      Votre navigateur ne supporte pas l'audio HTML5.
    </audio>

    <h1 class="start-button">BUZZEZ POUR COMMENCER</h1>

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
      this.playMusic()
      this.nextStep()
    },
    handleButtonPress(buttonId) {
      const validButtons = ['A', 'B', 'C', 'D']
      if (validButtons.includes(buttonId)) {
        this.playMusic()
        this.nextStep()
      }
    },
    playMusic() {
      const audio = this.$refs.bgMusic
      if (audio && audio.paused) {
        audio.play().catch(() => {
          // Gestion silencieuse en cas de blocage par le navigateur
        })
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
  border-top: 6px solid #330006;
  border-bottom: 6px solid #330006;
  border-left: none;
  border-right: none;
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
