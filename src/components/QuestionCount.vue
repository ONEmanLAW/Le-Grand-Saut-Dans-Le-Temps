<template>
  <div class="question-count-screen">
    <h2 class="title fade-in" style="animation-delay: 0s;">Choisissez le nombre de questions</h2>
    
    <div class="button-row">
      <button
        v-for="(count, index) in firstRow"
        :key="count"
        @click="selectCount(count)"
        class="fade-in"
        :style="{ 'animation-delay': `${0.3 + index * 0.2}s`, backgroundColor: buttonColors[index] }"
      >
        {{ count }}
      </button>
    </div>

    <div class="button-row">
      <button
        v-for="(count, index) in secondRow"
        :key="count"
        @click="selectCount(count)"
        class="fade-in"
        :style="{ 'animation-delay': `${0.7 + index * 0.2}s`, backgroundColor: buttonColors[index + 2] }"
      >
        {{ count }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionCount',
  props: {
    nextStep: Function,
    options: {
      type: Array,
      required: true
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
  data() {
    return {
      buttonColors: ['#FF6B6B', '#4ECDC4', '#556270', '#C7F464']
    }
  },
  methods: {
    selectCount(count) {
      localStorage.setItem('questionCount', count)
      this.nextStep()
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
  margin-bottom: 40px;
  justify-content: center;
}

button {
  width: 140px;
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
