<template>
  <div class="end-game-screen">
    <h1>Résultat final</h1>
    <p class="score">Score : {{ score }} / {{ questions }}</p>
    <p class="trophee" v-if="trophee">{{ tropheeMessage }}</p>
    <p v-else>Aucun trophée obtenu.</p>
    <button @click="replayGame">Rejouer</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      score: 0,
      questions: 0,
      trophee: ''
    }
  },
  computed: {
    tropheeMessage() {
      if (this.trophee === 'or') return "Trophée d'or 🎉"
      if (this.trophee === 'argent') return "Trophée d'argent 🥈"
      if (this.trophee === 'bronze') return "Trophée de bronze 🥉"
      return ''
    }
  },
  mounted() {
    this.score = parseInt(localStorage.getItem('score') || '0')
    this.questions = parseInt(localStorage.getItem('questionCount') || '0')
    this.determineTrophee()
  },
  methods: {
    determineTrophee() {
      const correctAnswers = this.score
      const questions = this.questions

      if (questions === 8) {
        if (correctAnswers >= 7) this.trophee = 'or'
        else if (correctAnswers >= 5) this.trophee = 'argent'
        else if (correctAnswers >= 4) this.trophee = 'bronze'
        else this.trophee = ''
      } else if (questions === 12) {
        if (correctAnswers >= 10) this.trophee = 'or'
        else if (correctAnswers >= 8) this.trophee = 'argent'
        else if (correctAnswers >= 6) this.trophee = 'bronze'
        else this.trophee = ''
      } else if (questions === 16) {
        if (correctAnswers >= 13) this.trophee = 'or'
        else if (correctAnswers >= 10) this.trophee = 'argent'
        else if (correctAnswers >= 8) this.trophee = 'bronze'
        else this.trophee = ''
      } else if (questions === 20) {
        if (correctAnswers >= 16) this.trophee = 'or'
        else if (correctAnswers >= 13) this.trophee = 'argent'
        else if (correctAnswers >= 10) this.trophee = 'bronze'
        else this.trophee = ''
      } else {
        this.trophee = ''
      }
    },
    replayGame() {
      localStorage.removeItem('score')
      localStorage.removeItem('questionCount')
      window.location.reload()
    }
  }
}
</script>

<style scoped>
.end-game-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
  background-color: #fafafa;
  padding: 20px;
  text-align: center;
}
.score {
  font-size: 3rem;
  font-weight: bold;
  margin: 20px 0;
}
.trophee {
  font-size: 2rem;
  margin-bottom: 40px;
  color: goldenrod;
}
button {
  font-size: 1.5rem;
  padding: 10px 30px;
  cursor: pointer;
}
button:hover {
  background-color: #eee;
}
</style>
