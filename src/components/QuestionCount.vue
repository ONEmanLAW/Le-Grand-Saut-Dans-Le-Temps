<template>
  <div class="question-count-screen">
    <h1 class="title fade-in" style="animation-delay: 0s;">Choisissez le nombre de questions</h1>
    
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
