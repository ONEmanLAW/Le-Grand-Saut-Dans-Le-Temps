<template>
  <div class="question-count-screen">
    <h1 class="title fade-in" style="animation-delay: 0.5s;">Choisissez le nombre de questions</h1>
    
    <div class="button-row">
      <div class="button-wrapper" v-for="(count, index) in firstRow" :key="count">
        <button
          @click="selectCount(count)"
          :disabled="!buttonsEnabled"
          :class="{ disabled: !buttonsEnabled }"
          :style="{
            'animation-delay': `${0.6 + index * 0.4}s`,
            backgroundColor: buttonColors[index]
          }"
        >
          {{ count }}
        </button>
      </div>
    </div>

    <div class="button-row">
      <div class="button-wrapper" v-for="(count, index) in secondRow" :key="count">
        <button
          @click="selectCount(count)"
          :disabled="!buttonsEnabled"
          :class="{ disabled: !buttonsEnabled }"
          :style="{
            'animation-delay': `${1.4 + index * 0.4}s`,
            backgroundColor: buttonColors[index + 2]
          }"
        >
          {{ count }}
        </button>
      </div>
    </div>

    <ButtonInputListener
      :active="buttonsEnabled"
      :onButtonPress="handleButtonPress"
    />
  </div>
</template>

<script>
import ButtonInputListener from './ButtonInputListener.vue'

export default {
  name: 'QuestionCount',
  components: { ButtonInputListener },
  props: {
    nextStep: Function,
    options: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      buttonColors: ['#47DEB1', '#FF8FC3', '#F16565', '#A695FF'],
      buttonsEnabled: false,
    }
  },
  computed: {
    firstRow() {
      return this.options.slice(0, 2)
    },
    secondRow() {
      return this.options.slice(2)
    }
  },
  mounted() {
    this.enableButtons()
    // Démarre la musique si elle n'existe pas encore
    if (!window.backgroundMusic) {
      const audio = new Audio('/audio/background.mp3')
      audio.loop = true
      audio.volume = 1
      // Tenter de jouer la musique, catch erreur autoplay si bloque
      audio.play().catch(() => {
        console.warn('Autoplay bloqué, musique démarrera après interaction utilisateur')
      })
      window.backgroundMusic = audio
    } else if (window.backgroundMusic.paused) {
      // Relance si en pause
      window.backgroundMusic.play().catch(() => {})
    }
  },
  methods: {
    enableButtons() {
      this.buttonsEnabled = true
    },
    disableButtons() {
      this.buttonsEnabled = false
    },
    selectCount(count) {
      if (!this.buttonsEnabled) return

      this.disableButtons()
      localStorage.setItem('questionCount', count)
      this.nextStep()
    },
    handleButtonPress(buttonId) {
      const buttonMap = { A: 0, B: 1, C: 2, D: 3 }
      const index = buttonMap[buttonId]

      if (index !== undefined && index < this.options.length) {
        this.selectCount(this.options[index])
      }
    }
  }
}
</script>

<style scoped>
.question-count-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px;
  box-sizing: border-box;
  overflow: visible;
}

.title {
  font-weight: bold;
  margin-bottom: 40px;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 1.2s ease-out forwards;
  width: 600px;
}

.button-row {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  justify-content: center;
  overflow: visible;
}

.button-wrapper {
  overflow: visible;
  margin-bottom: 40px;
  position: relative;
}

button {
  width: 560px;
  height: 225px;
  border: none;
  border-radius: 16px;
  font-weight: bold;
  cursor: pointer;
  opacity: 0;
  animation: fadeInUp 1.2s ease-out forwards;
  transition: filter 0.3s, opacity 0.3s;
  position: relative;
  z-index: 1;

  box-shadow: 0px 8px 10px rgba(0, 0, 0, 1);
}

button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
