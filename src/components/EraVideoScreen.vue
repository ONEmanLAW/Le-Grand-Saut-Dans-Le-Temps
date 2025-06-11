<template>
  <div class="start-screen">
    <div
      v-if="showText"
      class="start-text animated"
    >
      Bienvenue dans les années {{ selectedEra }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'EraIntroScreen',
  props: {
    nextStep: Function
  },
  data() {
    return {
      selectedEra: localStorage.getItem('selectedEra') || '',
      showText: false,
      audio: null
    }
  },
  mounted() {
    this.showText = true

    // Selon l'ère choisie, charge le son correspondant
    if (this.selectedEra === '50') {
      this.audio = new Audio('/audio/sound50troll.mp3')
    } else if (this.selectedEra === '80') {
      this.audio = new Audio('/audio/sound50troll.mp3')
    }

    if (this.audio) {
      this.audio.play().catch(() => {
        console.warn('Autoplay bloqué, le son sera joué après interaction')
      })
    }

    // Cache le texte après 4s
    setTimeout(() => {
      this.showText = false
    }, 4000)

    // Passe à l'étape suivante après 4s
    setTimeout(() => {
      if (typeof this.nextStep === 'function') {
        this.nextStep()
      }
    }, 4000)
  },
  beforeUnmount() {
    // Libère la ressource audio (optionnel)
    if (this.audio) {
      this.audio.pause()
      this.audio = null
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
  overflow: hidden;
}

.start-text {
  color: #330006;
  font-size: 64px;
  font-weight: bold;
  font-family: 'Berlin', sans-serif;
  text-transform: uppercase;
  padding: 40px 80px;
  border: 6px solid #330006;
  border-radius: 20px;
  text-align: center;
  opacity: 0;
}

.animated {
  animation: pulse-once 4s ease-in-out forwards;
}

@keyframes pulse-once {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  25% {
    transform: scale(1.1);
    opacity: 1;
  }
  75% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(0.8);
    opacity: 0;
  }
}
</style>
