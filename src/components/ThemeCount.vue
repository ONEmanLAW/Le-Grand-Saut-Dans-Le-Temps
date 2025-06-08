<template>
  <div class="theme-count-screen">
    <h1 class="title fade-in" style="animation-delay: 0s;">Choisissez un thème</h1>
    
    <div class="button-row">
      <div class="button-wrapper" v-for="(theme, index) in selectedThemes" :key="theme">
        <button
          @click="selectTheme(theme)"
          :disabled="!buttonsEnabled"
          :class="{ disabled: !buttonsEnabled }"
          :style="{
            'animation-delay': `${0.6 + index * 0.4}s`,
            backgroundColor: buttonColors[index]
          }"
        >
          {{ capitalize(theme) }}
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
  name: 'ThemeCount',
  components: { ButtonInputListener },
  props: {
    nextStep: Function,
    themes: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      selectedThemes: [],
      buttonColors: ['#47DEB1', '#F16565'],
      buttonsEnabled: false,
    }
  },
  mounted() {
    const shuffled = this.shuffleArray(this.themes)
    this.selectedThemes = shuffled.slice(0, 2)
    this.enableButtons()
  },
  methods: {
    enableButtons() {
      this.buttonsEnabled = true
    },
    disableButtons() {
      this.buttonsEnabled = false
    },
    selectTheme(theme) {
      if (!this.buttonsEnabled) return
      this.disableButtons()

      localStorage.setItem('selectedTheme', theme)
      this.nextStep()
    },
    shuffleArray(arr) {
      let array = arr.slice()
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[array[i], array[j]] = [array[j], array[i]]
      }
      return array
    },
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },
    handleButtonPress(buttonId) {
      const buttonMap = { A: 0, C: 1 }
      const index = buttonMap[buttonId]

      if (index !== undefined && index < this.selectedThemes.length) {
        this.selectTheme(this.selectedThemes[index])
      }
    }
  }
}
</script>

<style scoped>
.theme-count-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 40px;
  box-sizing: border-box;
  overflow: visible;
}

.title {
  font-weight: bold;
  margin-bottom: 60px;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 1.2s ease-out forwards;
  width: 600px; 
}

.button-row {
  display: flex;
  flex-direction: column;
  gap: 40px;
  justify-content: center;
  align-items: center;
  overflow: visible;
}

.button-wrapper {
  overflow: visible;
  margin-bottom: 30px; 
  position: relative;
  width: 1170px; 
}

button {
  width: 1170px;
  height: 225px;
  border: none;
  border-radius: 16px;
  color: black;
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
