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
      answerColors: ['#FF6B6B', '#4ECDC4', '#FFD166', '#80ED99'],
      isBeforeQuestion: false,
      isFeedback: false
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
        this.startNextQuestionCycle();
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
    startNextQuestionCycle() {
      this.isFeedback = false;
      this.prepareQuestionDisplay();
    },
    prepareQuestionDisplay() {
      this.preparingQuestion = true;
      this.questionNumberDisplay = `QUESTION ${this.totalQuestionsAsked + 1}`;
      setTimeout(() => {
        this.preparingQuestion = false;
        this.loadBeforeQuestionOrQuestion();
      }, 2000);
    },
    loadBeforeQuestionOrQuestion() {
      const currentQuestionData = this.questionsInCurrentDifficulty[this.currentQuestionIndexInLevel];
      if (currentQuestionData?.beforeQuestion) {
        this.currentQuestion = currentQuestionData;
        this.isBeforeQuestion = true;
      } else {
        this.isBeforeQuestion = false;
        this.loadQuestion();
      }
    },
    startQuestion() {
      this.isBeforeQuestion = false;
      this.loadQuestion();
      if (this.$refs.beforeQuestionAudio) {
        this.$refs.beforeQuestionAudio.pause();
        this.$refs.beforeQuestionAudio.currentTime = 0;
      }
    },
    loadQuestion() {
      clearTimeout(this.timeoutId);
      this.transitionVideo = false;
      const questions = this.questionsInCurrentDifficulty;
      if (questions && this.currentQuestionIndexInLevel < questions.length && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        this.currentQuestion = questions[this.currentQuestionIndexInLevel];
        this.selectedAnswer = null;
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
          this.isFeedback = true;
          if (this.currentQuestion?.feedback?.audio && this.$refs.feedbackAudio) {
            this.$refs.feedbackAudio.play();
          }
        }, 2000);
      }
    },
    nextStepAfterFeedback() {
      this.isFeedback = false;
      this.totalQuestionsAsked++;
      this.moveToNextStep();
    },
    moveToNextStep() {
      if (this.currentQuestionIndexInLevel < this.questionsPerLevel - 1) {
        this.currentQuestionIndexInLevel++;
        this.startNextQuestionCycle();
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
      this.startNextQuestionCycle();
    }
  }
};
</script>

<template>
  <div class="question-screen" :class="{'answered-state': answered, 'before-question-state': isBeforeQuestion, 'feedback-state': isFeedback}">
    <div v-if="loading">Chargement des questions...</div>
    <div v-else-if="error">Erreur : {{ error }}</div>

    <div v-else-if="preparingQuestion">
      <div class="fullscreen-message">
        <h1>{{ questionNumberDisplay }}</h1>
      </div>
    </div>

    <div v-else-if="isBeforeQuestion && currentQuestion?.beforeQuestion">
      <div class="before-question-content">
        <h2 v-if="currentQuestion.beforeQuestion.text">{{ currentQuestion.beforeQuestion.text }}</h2>
        <audio v-if="currentQuestion.beforeQuestion.audio" ref="beforeQuestionAudio" :src="currentQuestion.beforeQuestion.audio" controls autoplay @ended="startQuestion"></audio>
        <button v-else @click="startQuestion" class="start-button">Commencer la question</button>
      </div>
    </div>

    <div v-else-if="isFeedback && currentQuestion?.feedback">
      <div class="feedback-content">
        <h2>Feedback</h2>
        <img v-if="currentQuestion.feedback.image" :src="currentQuestion.feedback.image" alt="Feedback Image" class="feedback-image">
        <p v-if="currentQuestion.feedback.text" class="feedback-text">{{ currentQuestion.feedback.text }}</p>
        <audio v-if="currentQuestion.feedback.audio" ref="feedbackAudio" :src="currentQuestion.feedback.audio" controls autoplay @ended="nextStepAfterFeedback"></audio>
        <button v-else @click="nextStepAfterFeedback" class="next-button">Suivant</button>
      </div>
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

<style scoped>
/* Styles existants */
.question-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 40px;
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
  text-align: center;
}

.question-number {
  color: #555;
  margin-bottom: 10px;
  font-size: 1.1em;
  align-self: flex-start;
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
  background-color: inherit;
}

.answers-grid button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.answers-grid li.correct {
  grid-column: 1 / -1;
  justify-self: center;
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
  display: block;
}

.question-screen.answered-state h2 {
  opacity: 0.5;
}

/* Styles pour l'écran "Before Question" */
.before-question-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.before-question-content h2 {
  margin-bottom: 20px;
}

.before-question-content audio {
  margin-bottom: 20px;
}

.before-question-content .start-button {
  padding: 15px 30px;
  font-size: 1.2em;
  cursor: pointer;
  border: none;
  border-radius: 8px;
  background-color: #007bff;
  color: white;
  transition: background-color 0.3s ease;
}

.before-question-content .start-button:hover {
  background-color: #0056b3;
}

/* Styles pour l'écran de feedback */
.feedback-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feedback-content h2 {
  margin-bottom: 20px;
}

.feedback-content img {
  max-width: 300px;
  margin-bottom: 20px;
  border-radius: 8px;
}

.feedback-content p {
  font-size: 1.1em;
  margin-bottom: 20px;
}

.feedback-content audio {
  margin-bottom: 20px;
}

.feedback-content .next-button {
  padding: 15px 30px;
  font-size: 1.2em;
  cursor: pointer;
  border: none;
  border-radius: 8px;
  background-color: #28a745;
  color: white;
  transition: background-color 0.3s ease;
}

.feedback-content .next-button:hover {
  background-color: #1e7e34;
}
</style>