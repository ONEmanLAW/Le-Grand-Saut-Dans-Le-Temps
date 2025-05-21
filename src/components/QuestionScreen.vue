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
      totalQuestionsToAsk: 0
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
        this.loadQuestionForLevel();
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
        this.totalQuestionsAsked++; // Incrémenter immédiatement après la réponse

        this.timeoutId = setTimeout(() => {
          this.moveToNextStep();
        }, 2000);
      }
    },
    moveToNextStep() {
      if (this.currentQuestionIndexInLevel < this.questionsPerLevel - 1) {
        this.currentQuestionIndexInLevel++;
        this.loadQuestionForLevel();
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
      this.loadQuestionForLevel();
    }
  }
};
</script>

<template>
  <div class="question-screen">
    <div v-if="loading">Chargement des questions...</div>
    <div v-else-if="error">Erreur : {{ error }}</div>
    <div v-else-if="transitionVideo && transitionVideoSource">
      <h2>Préparation du niveau suivant...</h2>
      <video ref="transitionVideoPlayer" @ended="nextLevel" autoplay>
        <source :src="transitionVideoSource" type="video/mp4">
        Votre navigateur ne supporte pas la lecture de vidéos.
      </video>
    </div>
    <div v-else-if="currentQuestion">
      <h2>{{ currentQuestion.question }}</h2>
      <ul>
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
          >{{ answer }}</button>
        </li>
      </ul>
      <p v-if="totalQuestionsToAsk > 0">Question {{ totalQuestionsAsked + 1 }} / {{ totalQuestionsToAsk }}</p>
    </div>
    <div v-else>
      <p>{{ feedback || 'Fin de la partie !' }}</p>
    </div>
  </div>
</template>

<style scoped>
.question-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

ul {
  list-style: none;
  padding: 0;
  margin-bottom: 30px;
  width: 100%;
  max-width: 500px;
}

li {
  margin: 10px 0;
}

button {
  display: block;
  width: 100%;
  padding: 15px 25px;
  font-size: 18px;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: white;
  color: #333;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: #e0e0e0;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.correct button {
  background-color: #aaff80; /* Vert clair */
  color: #333;
  font-weight: bold;
}

.incorrect button {
  background-color: #ff8080; /* Rouge clair */
  color: white;
}

.hidden {
  opacity: 0.5;
}

.feedback {
  margin-top: 20px;
  font-weight: bold;
  color: #555;
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
</style>