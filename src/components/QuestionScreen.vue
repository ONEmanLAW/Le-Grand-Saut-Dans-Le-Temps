<template>
  <div class="question-screen" :class="{'answered-state': answered}">
    <div v-if="loading">Chargement des questions...</div>
    <div v-else-if="error">Erreur : {{ error }}</div>
    <div v-else-if="preparingQuestion">
      <div class="fullscreen-message">
        <h1>{{ questionNumberDisplay }}</h1>
      </div>
    </div>
    <div v-else-if="transitionVideo && transitionVideoSource">
      <h2>Préparation du niveau suivant...</h2>
      <video ref="transitionVideoPlayer" @ended="nextLevel" autoplay>
        <source :src="transitionVideoSource" type="video/mp4">
        Votre navigateur ne supporte pas la lecture de vidéos.
      </video>
    </div>
    <div v-else-if="currentQuestion">
      <p v-if="totalQuestionsToAsk > 0" class="question-number">Question {{ totalQuestionsAsked + 1 }} / {{ totalQuestionsToAsk }}</p>
      <h2>{{ currentQuestion.question }}</h2>
      <ul class="answers-grid">
        <li
          v-for="(answer, index) in currentQuestion.answers"
          :key="index"
          :class="{
            'correct': answered && index === currentQuestion.correctIndex,
            'incorrect': answered && index === selectedAnswer && index !== currentQuestion.correctIndex,
            'hidden': answered && index !== currentQuestion.correctIndex && index !== selectedAnswer
          }"
        >
          <button
            @click="selectAnswer(index)"
            :disabled="answered"
            :style="{ backgroundColor: answerColors[index % answerColors.length] }"
          >{{ answer }}</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>{{ feedback || 'Fin de la partie !' }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: ['flowObject'],
  data() {
    return {
      questionsData: null,
      currentQuestionIndexInLevel: 0,
      currentDifficultyIndex: 0,
      difficulties: ['easy', 'medium', 'hard', 'expert'],
      transitionVideos: {
        'easy': '/videos/medium.mp4',
        'medium': '/videos/hard.mp4',
        'hard': '/videos/expert.mp4'
      },
      currentQuestion: null,
      selectedAnswer: null,
      feedback: '',
      answered: false,
      currentTheme: '',
      loading: true,
      error: null,
      timeoutId: null,
      transitionVideo: false,
      transitionVideoSource: '',
      questionsPerLevel: 0,
      totalQuestionsAsked: 0,
      totalQuestionsToAsk: 0,
      preparingQuestion: false,
      questionNumberDisplay: '',
      answerColors: ['#FF6B6B', '#4ECDC4', '#FFD166', '#80ED99'] // Tableau de couleurs pour les boutons
    };
  },
  async mounted() {
    const era = localStorage.getItem('selectedEra');
    this.currentTheme = localStorage.getItem('selectedTheme');
    this.totalQuestionsToAsk = parseInt(localStorage.getItem('questionCount') || '0');

    let questionsFile = '';
    if (era === '80') {
      questionsFile = '/data/questions_80.json';
    } else {
      questionsFile = '/data/questions_50.json';
    }

    if (this.currentTheme && this.totalQuestionsToAsk > 0) {
      this.questionsPerLevel = Math.floor(this.totalQuestionsToAsk / this.difficulties.length);
      try {
        const response = await fetch(questionsFile);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.questionsData = await response.json();
        this.prepareNextQuestionDisplay();
        this.loading = false;
      } catch (e) {
        this.error = e;
        this.loading = false;
        console.error("Erreur lors du chargement des questions :", e);
      }
    } else {
      this.error = 'Thème ou nombre de questions non défini.';
      this.loading = false;
    }
  },
  computed: {
    currentDifficulty() {
      return this.difficulties[this.currentDifficultyIndex];
    },
    questionsInCurrentDifficulty() {
      return this.questionsData?.[this.currentTheme]?.[this.currentDifficulty] || [];
    }
  },
  methods: {
    prepareNextQuestionDisplay() {
      this.preparingQuestion = true;
      this.questionNumberDisplay = `QUESTION ${this.totalQuestionsAsked + 1}`;
      setTimeout(() => {
        this.preparingQuestion = false;
        this.loadQuestionForLevel();
      }, 2000);
    },
    loadQuestionForLevel() {
      clearTimeout(this.timeoutId);
      this.transitionVideo = false;
      const questions = this.questionsInCurrentDifficulty;
      if (questions && this.currentQuestionIndexInLevel < questions.length && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        this.currentQuestion = questions[this.currentQuestionIndexInLevel];
        this.selectedAnswer = null;
        this.feedback = '';
        this.answered = false;
      } else {
        this.startTransitionOrEnd();
      }
    },
    selectAnswer(index) {
      if (!this.answered && this.currentQuestion && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        this.selectedAnswer = index;
        this.answered = true;
        const isCorrect = index === this.currentQuestion.correctIndex;
        this.feedback = isCorrect ? 'Correct !' : `Incorrect. La bonne réponse était : ${this.currentQuestion.answers[this.currentQuestion.correctIndex]}`;

        this.timeoutId = setTimeout(() => {
          this.totalQuestionsAsked++;
          this.moveToNextStep();
        }, 2000);
      }
    },
    moveToNextStep() {
      if (this.currentQuestionIndexInLevel < this.questionsPerLevel - 1) {
        this.currentQuestionIndexInLevel++;
        this.prepareNextQuestionDisplay();
      } else {
        this.startTransitionOrEnd();
      }
    },
    startTransitionOrEnd() {
      if (this.currentDifficultyIndex < this.difficulties.length - 1 && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        this.transitionVideo = true;
        this.transitionVideoSource = this.transitionVideos[this.difficulties[this.currentDifficultyIndex]] || '';
        this.$nextTick(() => {
          if (this.$refs.transitionVideoPlayer && this.transitionVideoSource) {
            this.$refs.transitionVideoPlayer.play();
          } else {
            this.nextLevel();
          }
        });
      } else {
        this.currentQuestion = null;
        this.feedback = 'Fin de la partie !';
      }
    },
    nextLevel() {
      this.currentDifficultyIndex++;
      this.currentQuestionIndexInLevel = 0;
      this.prepareNextQuestionDisplay();
    }
  }
};
</script>

<style scoped>
.question-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* Centrer verticalement le contenu principal */
  min-height: 100vh;
  padding: 40px;
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
  text-align: center; /* Centrer le texte des éléments enfants par défaut */
}

.question-number {
  color: #555;
  margin-bottom: 10px;
  font-size: 1.1em;
  align-self: flex-start; /* Aligner à gauche */
  margin-left: auto;
  margin-right: auto;
}

h2 {
  color: #333;
  margin-bottom: 30px;
}

.answers-grid {
  list-style: none;
  padding: 0;
  margin-bottom: 30px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.answers-grid li {
  margin: 0;
  opacity: 1;
  transition: opacity 0.3s ease, transform 0.3s ease;
  display: flex;
  justify-content: center;
}

.answers-grid button {
  display: block;
  width: 100%;
  padding: 15px 25px;
  font-size: 18px;
  cursor: pointer;
  border: none;
  border-radius: 8px;
  color: white;
  transition: transform 0.3s ease, opacity 0.3s ease;
  box-sizing: border-box;
  background-color: inherit; /* Hérite de la couleur définie par :style */
}

.answers-grid button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.answers-grid li.correct {
  grid-column: 1 / -1; /* Prend toute la largeur de la grille */
  justify-self: center; /* Se centre horizontalement dans la grille */
  animation: moveToCenter 0.5s ease-out forwards;
}

.answers-grid li.correct button {
  color: #333;
  font-weight: bold;
}

.answers-grid li.incorrect {
  opacity: 0;
}

.hidden {
  display: none;
}

video {
  width: 80%;
  max-width: 600px;
  margin-top: 30px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

p {
  color: #555;
  margin-top: 15px;
  text-align: center;
}

.fullscreen-message {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  color: white;
  font-size: 48px;
  font-weight: bold;
}

@keyframes moveToCenter {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Styles spécifiques après la réponse */
.question-screen.answered-state .answers-grid {
  /* La disposition est gérée par les styles ci-dessus */
}

.question-screen.answered-state .answers-grid li:not(.correct) {
  opacity: 0;
  display: block; /* Pour que l'animation d'opacité fonctionne */
}

.question-screen.answered-state h2 {
  opacity: 0.5; /* Légèrement estompé après la réponse */
}
</style>