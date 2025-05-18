<template>
  <div class="theme-count-screen">
    <h2 class="title fade-in" style="animation-delay: 0s;">Choisissez un thème</h2>
    <div class="button-row">
      <button
        v-for="(theme, index) in selectedThemes"
        :key="theme"
        @click="selectTheme(theme)"
        class="fade-in"
        :style="{ 'animation-delay': `${0.3 + index * 0.2}s`, backgroundColor: buttonColors[index] }"
      >
        {{ capitalize(theme) }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ThemeCount',
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
      buttonColors: ['#FF6B6B', '#4ECDC4']
    }
  },
  methods: {
    selectTheme(theme) {
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
    }
  },
  mounted() {
    // Sélectionner 2 thèmes aléatoires parmi les props.themes
    const shuffled = this.shuffleArray(this.themes)
    this.selectedThemes = shuffled.slice(0, 2)
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
}

.title {
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 60px;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 0.6s forwards;
}

.button-row {
  display: flex;
  gap: 40px;
  justify-content: center;
}

button {
  width: 180px;
  height: 80px;
  font-size: 28px;
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
  opacity: 0;
  animation: fadeInUp 0.6s forwards;
  transition: filter 0.3s;
}

button:hover {
  filter: brightness(85%);
}

/* Animation fadeInUp */
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
