<template>
  <div class="question-count-screen">
    <h1 class="title fade-in" style="animation-delay: 0s;">Choisissez le nombre de questions</h1>
    
    <div class="button-row">
      <button
        v-for="(count, index) in firstRow"
        :key="count"
        @click="selectCount(count)"
        :disabled="!buttonsEnabled"
        :style="{
          'animation-delay': `${0.3 + index * 0.2}s`,
          backgroundColor: buttonColors[index],
          opacity: buttonsEnabled ? 1 : 0.5,
          cursor: buttonsEnabled ? 'pointer' : 'not-allowed'
        }"
      >
        {{ count }}
      </button>
    </div>

    <div class="button-row">
      <button
        v-for="(count, index) in secondRow"
        :key="count"
        @click="selectCount(count)"
        :disabled="!buttonsEnabled"
        :style="{
          'animation-delay': `${0.7 + index * 0.2}s`,
          backgroundColor: buttonColors[index + 2],
          opacity: buttonsEnabled ? 1 : 0.5,
          cursor: buttonsEnabled ? 'pointer' : 'not-allowed'
        }"
      >
        {{ count }}
      </button>
    </div>

    <!-- Composant ButtonInputListener -->
    <ButtonInputListener
      :active="buttonsEnabled"
      :onButtonPress="handleButtonPress"
    />
  </div>
</template>

<script>
import ButtonInputListener from './ButtonInputListener.vue' // ajuste le chemin si besoin

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
      buttonColors: ['#FF6B6B', '#4ECDC4', '#556270', '#C7F464'],
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
      // Par exemple, ici tu fais correspondre les boutons A, B, C, D aux options
      // Ou adapte selon ta logique, ici on suppose juste un mapping simple
      // Si tu as 4 options, A->options[0], B->options[1], etc.
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
  height: 100vh;
  padding: 40px;
  box-sizing: border-box;
}

.title {
  font-weight: bold;
  margin-bottom: 80px;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 0.6s forwards;
  width: 600px;
}

.button-row {
  display: flex;
  gap: 60px;
  margin-bottom: 60px;
  justify-content: center;
}

button {
  width: 454px;
  height: 180px;
  border: 3px solid black;
  border-radius: 16px;
  color: black;
  font-weight: bold;
  cursor: pointer;
  opacity: 0;
  animation: fadeInUp 0.6s forwards;
  transition: filter 0.3s;
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
