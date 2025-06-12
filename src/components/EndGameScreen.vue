<!-- EndGameScreen.vue -->
<template>
  <div class="end-game-screen">
    <!-- Musique de fond -->
    <audio ref="bgMusic" autoplay loop>
      <source src="/audio/backgroundEnd.mp3" type="audio/mpeg" />
      Votre navigateur ne supporte pas l'audio HTML5.
    </audio>

    <h1 class="congrats"> Félicitations ! </h1>
    <p class="finished">Vous avez terminé tous les niveaux du jeu.</p>
    
    <p class="score">Score : {{ score }} / {{ questions }}</p>
    
    <div class="trophee-container" v-if="trophee">
      <p class="trophee-message">{{ tropheeMessage }}</p>
    </div>
    <p v-else class="no-trophee">Aucun trophée obtenu.</p>

    <div class="button-row">
      <div class="button-wrapper">
        <button
          @click="replayGame"
          :disabled="buttonsDisabled"
          :class="{ disabled: buttonsDisabled }"
        >
          Rejouer
        </button>
      </div>
    </div>

    <!-- Écouteur de bouton A, B, C, D -->
    <ButtonInputListener
      :onButtonPress="handleButtonPress"
      :active="true"
    />
  </div>
</template>

<script>
import confetti from 'canvas-confetti'
import ButtonInputListener from './ButtonInputListener.vue'

export default {
  components: { ButtonInputListener },
  data() {
    return {
      score: 0,
      questions: 0,
      trophee: '',
      buttonsDisabled: true
    }
  },
  computed: {
    tropheeMessage() {
      if (this.trophee === 'or') return "Trophée d'or"
      if (this.trophee === 'argent') return "Trophée d'argent"
      if (this.trophee === 'bronze') return "Trophée de bronze"
      return ''
    }
  },
  mounted() {
    this.score = parseInt(localStorage.getItem('score') || '0')
    this.questions = parseInt(localStorage.getItem('questionCount') || '0')
    this.determineTrophee()
    this.launchConfetti()
    this.playMusic()
  },
  methods: {
    playMusic() {
      const audio = this.$refs.bgMusic
      if (audio && audio.paused) {
        audio.play().catch(() => {
          // En cas de blocage du navigateur (auto-play policy)
        })
      }
    },
    determineTrophee() {
      const correctAnswers = this.score
      const questions = this.questions

      if (questions === 4) {
        if (correctAnswers === 4) this.trophee = 'or'
        else if (correctAnswers === 3) this.trophee = 'argent'
        else if (correctAnswers === 2) this.trophee = 'bronze'
        else this.trophee = 'none'
      } else if (questions === 8) {
        if (correctAnswers >= 7) this.trophee = 'or'
        else if (correctAnswers >= 5) this.trophee = 'argent'
        else if (correctAnswers >= 4) this.trophee = 'bronze'
        else this.trophee = 'none'
      } else if (questions === 12) {
        if (correctAnswers >= 10) this.trophee = 'or'
        else if (correctAnswers >= 8) this.trophee = 'argent'
        else if (correctAnswers >= 6) this.trophee = 'bronze'
        else this.trophee = 'none'
      } else if (questions === 16) {
        if (correctAnswers >= 13) this.trophee = 'or'
        else if (correctAnswers >= 10) this.trophee = 'argent'
        else if (correctAnswers >= 8) this.trophee = 'bronze'
        else this.trophee = 'none'
      } else {
        this.trophee = 'none'
      }
    },
    launchConfetti() {
      const duration = 10000
      const animationEnd = Date.now() + duration
      const defaults = {
        startVelocity: 40,
        spread: 360,
        ticks: 60,
        gravity: 0.5,
        scalar: 1.5,
        origin: { y: 0 }
      }

      const interval = setInterval(() => {
        const timeLeft = animationEnd - Date.now()
        if (timeLeft <= 0) {
          clearInterval(interval)
          return
        }

        const particleCount = 100 * (timeLeft / duration)

        confetti(Object.assign({}, defaults, {
          particleCount,
          origin: { x: Math.random(), y: 0 }
        }))
      }, 200)
    },
    replayGame() {
      localStorage.removeItem('score')
      localStorage.removeItem('questionCount')
      window.location.reload()
    },
    handleButtonPress(button) {
      if (button === 'A') {
        this.replayGame()
      }
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
  padding: 20px;
  text-align: center;
}

.congrats {
  font-size: 72px;
  margin-bottom: 40px;
}

.finished {
  font-size: 48px;
  margin-bottom: 40px;
  color: #330006;
}

.score {
  font-size: 64px;
  font-weight: bold;
  margin-bottom: 40px;
  color: #330006;
}

.trophee-message {
  font-size: 48px;
  margin-bottom: 40px;
}

.no-trophee {
  font-size: 48px;
  margin-bottom: 40px;
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
  margin-bottom: 40px;
  position: relative;
  width: 1160px;
}

button {
  width: 1160px;
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
  background-color: #47DEB1;
}

button:hover {
  filter: brightness(1.1);
}

button.disabled,
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(40px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
