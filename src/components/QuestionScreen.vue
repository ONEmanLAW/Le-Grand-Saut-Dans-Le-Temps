<script>
export default {
  props: ['flowObject', 'nextStep'],
  data() {
    return {
      questionsData: null,
      currentQuestionIndexInLevel: 0,
      currentDifficultyIndex: 0,
      difficulties: ['easy', 'medium', 'hard', 'expert'],
      transitionVideos: {
        medium: {
          bien: '/videos/medium_bien.mp4',
          pasBien: '/videos/introHistory.mp4',
        },
        hard: {
          bien: '/videos/hard_bien.mp4',
          pasBien: '/videos/introHistory.mp4',
        },
        expert: {
          bien: '/videos/expert_bien.mp4',
          pasBien: '/videos/introHistory.mp4',
        }
      },
      endVideos: {
        bien: '/videos/endVideo.mp4',
        pasBien: '/videos/introHistory.mp4',
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
      isFeedback: false,
      gameFinished: false,
      score: 0,
      levelScores: {
        easy: 0,
        medium: 0,
        hard: 0,
        expert: 0
      },
      isEndVideoPlaying: false
    };
  },
  async mounted() {
    const era = localStorage.getItem('selectedEra');
    this.currentTheme = localStorage.getItem('selectedTheme');
    this.totalQuestionsToAsk = parseInt(localStorage.getItem('questionCount') || '0');
    let questionsFile = era === '80' ? '/data/questions_80.json' : '/data/questions_50.json';

    if (this.currentTheme && this.totalQuestionsToAsk > 0) {
      this.questionsPerLevel = Math.floor(this.totalQuestionsToAsk / this.difficulties.length);
      console.log("🧠 Chargement des questions, questionsParNiveau :", this.questionsPerLevel);

      try {
        const response = await fetch(questionsFile);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        this.questionsData = await response.json();
        this.startNextQuestionCycle();
        this.loading = false;
      } catch (e) {
        this.error = e;
        this.loading = false;
        console.error("❌ Erreur de chargement des questions :", e);
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
      this.isEndVideoPlaying = false;
      const questions = this.questionsInCurrentDifficulty;
      if (
        this.currentQuestionIndexInLevel < this.questionsPerLevel &&
        this.totalQuestionsAsked < this.totalQuestionsToAsk
      ) {
        const questions = this.questionsInCurrentDifficulty;

        // Si la question demandée dépasse les questions disponibles, recycle depuis le début
        const index = this.currentQuestionIndexInLevel % questions.length;
        this.currentQuestion = questions[index];

        this.selectedAnswer = null;
        this.answered = false;
      } else {
        console.log("🔄 Fin de niveau ou de questions, transition...");
        this.startTransitionOrEnd();
      }
    },
    selectAnswer(index) {
      if (!this.answered && this.currentQuestion && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        this.selectedAnswer = index;
        this.answered = true;
        const isCorrect = index === this.currentQuestion.correctIndex;
        if (isCorrect) {
          this.score++;
          this.levelScores[this.currentDifficulty]++;
        }

        this.feedback = isCorrect ? 'Correct !' : `Incorrect. La bonne réponse était : ${this.currentQuestion.answers[this.currentQuestion.correctIndex]}`;

        this.timeoutId = setTimeout(() => {
          this.isFeedback = true;
          if (this.currentQuestion?.feedback?.audio && this.$refs.feedbackAudio) {
            this.$refs.feedbackAudio.play();
          } else {
            setTimeout(() => {
              this.nextStepAfterFeedback();
            }, 3000);
          }
        }, 2000);
      }
    },
    nextStepAfterFeedback() {
      this.isFeedback = false;
      this.totalQuestionsAsked++;
      console.log("✅ Réponse terminée, totalQuestionsAsked :", this.totalQuestionsAsked);

      if (this.totalQuestionsAsked >= this.totalQuestionsToAsk) {
        this.playEndVideo();
      } else {
        this.moveToNextStep();
      }
    },
    moveToNextStep() {
      this.currentQuestionIndexInLevel++;
      if (this.currentQuestionIndexInLevel < this.questionsPerLevel) {
        console.log("➡️ Question suivante dans le même niveau :", this.currentDifficulty);
        this.startNextQuestionCycle();
      } else {
        console.log("🏁 Niveau terminé :", this.currentDifficulty);
        this.startTransitionOrEnd();
      }
    },
    startTransitionOrEnd() {
      if (this.currentDifficulty === 'expert') {
        console.log("🎬 Fin de partie : lecture de la vidéo de fin");
        this.playEndVideo();
        return;
      }

      const nextDifficulty = this.difficulties[this.currentDifficultyIndex + 1];

      if (this.currentDifficultyIndex < this.difficulties.length - 1 && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        this.transitionVideo = true;

        const seuilMoyen = Math.ceil(this.questionsPerLevel / 2);
        const scoreNiveauPrecedent = this.levelScores[this.currentDifficulty];

        this.transitionVideoSource =
          scoreNiveauPrecedent >= seuilMoyen
            ? this.transitionVideos[nextDifficulty]?.bien
            : this.transitionVideos[nextDifficulty]?.pasBien;

        console.log("🎥 Transition vers :", nextDifficulty, "| Vidéo :", this.transitionVideoSource);

        this.$nextTick(() => {
          if (this.$refs.transitionVideoPlayer && this.transitionVideoSource) {
            console.log("▶️ Lecture de la vidéo de transition...");
            this.$refs.transitionVideoPlayer.play();
          } else {
            console.warn("⚠️ Vidéo de transition manquante ou ref non trouvé");
            this.nextLevel();
          }
        });
      } else {
        console.log("🎬 Plus de niveaux ou questions, vidéo de fin");
        this.playEndVideo();
      }
    },
    nextLevel() {
      this.currentDifficultyIndex++;
      this.currentQuestionIndexInLevel = 0;
      console.log("⬆️ Passage au niveau suivant :", this.currentDifficulty);
      this.startNextQuestionCycle();
    },
    playEndVideo() {
      this.transitionVideo = true;
      this.isEndVideoPlaying = true;

      const seuilMoyen = Math.ceil(this.questionsPerLevel / 2);
      const scoreExpert = this.levelScores.expert;

      this.transitionVideoSource =
        scoreExpert >= seuilMoyen ? this.endVideos.bien : this.endVideos.pasBien;

      console.log("🎬 Vidéo de fin choisie :", this.transitionVideoSource);

      this.$nextTick(() => {
        if (this.$refs.transitionVideoPlayer && this.transitionVideoSource) {
          console.log("▶️ Lecture de la vidéo de fin...");
          this.$refs.transitionVideoPlayer.play();
        } else {
          console.warn("⚠️ Vidéo de fin non trouvée");
          this.finishGame();
        }
      });
    },
    onTransitionVideoEnded() {
      if (this.isEndVideoPlaying) {
        this.isEndVideoPlaying = false;
        console.log("✅ Vidéo de fin terminée");
        this.finishGame();
      } else {
        console.log("✅ Vidéo de transition terminée, passage au niveau suivant");
        this.transitionVideo = false;
        this.nextLevel();
      }
    },
    finishGame() {
      this.gameFinished = true;
      this.currentQuestion = null;
      this.feedback = 'Fin de la partie !';
      localStorage.setItem('score', this.score.toString());
      localStorage.setItem('questionCount', this.totalQuestionsAsked.toString());
      console.log("🏁 Fin du jeu. Score :", this.score);

      if (this.nextStep) {
        this.nextStep();
      } else {
        console.warn('nextStep() non défini dans QuestionScreen');
      }
    }
  }
};
</script>





<template>
  <div
    class="question-screen"
    :class="{
      'answered-state': answered,
      'before-question-state': isBeforeQuestion,
      'feedback-state': isFeedback
    }"
  >
    <div v-if="loading">Chargement des questions...</div>
    <div v-else-if="error">Erreur : {{ error }}</div>

    <div v-else-if="preparingQuestion">
      <div class="fullscreen-message">
        <h1>{{ questionNumberDisplay }}</h1>
      </div>
    </div>

    <!-- Video de transition ou de fin -->
    <div v-if="transitionVideo && transitionVideoSource">
      <video
        ref="transitionVideoPlayer"
        :src="transitionVideoSource"
        autoplay
        playsinline
        class="transition-video"
        @ended="onTransitionVideoEnded"
        controls="false"
      ></video>
    </div>

    <div v-else-if="isBeforeQuestion && currentQuestion?.beforeQuestion">
      <div class="before-question-content">
        <h2 v-if="currentQuestion.beforeQuestion.text">{{ currentQuestion.beforeQuestion.text }}</h2>
        <audio
          v-if="currentQuestion.beforeQuestion.audio"
          ref="beforeQuestionAudio"
          :src="currentQuestion.beforeQuestion.audio"
          controls
          autoplay
          @ended="startQuestion"
        ></audio>
        <button v-else @click="startQuestion" class="start-button">
          Commencer la question
        </button>
      </div>
    </div>

    <div v-else-if="isFeedback && currentQuestion?.feedback">
      <div class="feedback-content">
        <h2>Feedback</h2>
        <img
          v-if="currentQuestion.feedback.image"
          :src="currentQuestion.feedback.image"
          alt="Feedback Image"
          class="feedback-image"
        />
        <p v-if="currentQuestion.feedback.text" class="feedback-text">
          {{ currentQuestion.feedback.text }}
        </p>
        <audio
          v-if="currentQuestion.feedback.audio"
          ref="feedbackAudio"
          :src="currentQuestion.feedback.audio"
          autoplay
          @ended="nextStepAfterFeedback"
        ></audio>
      </div>
    </div>

    <div v-else-if="currentQuestion">
      <p v-if="totalQuestionsToAsk > 0" class="question-number">
        Question {{ totalQuestionsAsked + 1 }} / {{ totalQuestionsToAsk }}
      </p>
      <h2>{{ currentQuestion.question }}</h2>
      <ul class="answers-grid" :data-count="currentQuestion.answers.length">
        <li
          v-for="(answer, index) in currentQuestion.answers"
          :key="index"
          :class="{
            correct: answered && index === currentQuestion.correctIndex,
            incorrect: answered && index === selectedAnswer && index !== currentQuestion.correctIndex,
            hidden: answered && index !== currentQuestion.correctIndex && index !== selectedAnswer
          }"
        >
          <button
            @click="selectAnswer(index)"
            :disabled="answered"
            :style="{ backgroundColor: answerColors[index % answerColors.length] }"
          >
            {{ answer }}
          </button>
        </li>
      </ul>
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
  justify-content: center;
  min-height: 100vh;
  padding: 40px;
  font-family: 'Arial', sans-serif;
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
  display: grid;
  justify-content: center; /* centre la grille horizontale */
  gap: 20px;
}

.answers-grid[data-count="2"] {
  grid-template-columns: 1fr;
  width: fit-content; /* largeur juste ce qu'il faut */
  margin: 0 auto; /* centre horizontalement le container */
}

.answers-grid[data-count="4"] {
  grid-template-columns: repeat(2, 1fr);
  width: fit-content;
  margin: 0 auto; /* centre horizontalement */
  gap: 20px 40px;
}

.answers-grid li {
  display: flex;
  justify-content: center; /* centre horizontalement le bouton dans son li */
  width: auto; /* pas de largeur fixe, prend la largeur du bouton */
}

.answers-grid button {
  width: 454px;
  height: 180px;
  font-size: 48px;
  font-weight: bold;
  cursor: pointer;
  border: 3px solid black;
  border-radius: 16px;
  color: black;
  background-color: transparent;
  transition: filter 0.3s ease, background-color 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  box-sizing: border-box;
  position: relative; /* nécessaire pour positionner le trait blanc */
}

/* Trait blanc sous le bouton */
.answers-grid button::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: 2.5%;
  width: 95%;
  height: 8px;
  background-color: white;
  opacity: 0.7;
}

.answers-grid button:hover:not(:disabled) {
  filter: brightness(85%);
  background-color: rgba(0, 0, 0, 0.05);
}

.answers-grid button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* États correct / incorrect */
.answers-grid li.correct button {
  border-color: #28a745;
  color: #28a745;
}

.answers-grid li.incorrect button {
  border-color: #dc3545;
  color: #dc3545;
}

/* Après réponse, cacher les boutons non corrects */
.question-screen.answered-state .answers-grid li:not(.correct) {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.hidden {
  display: none;
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

/* Styles "Before Question" */
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

/* Styles Feedback */
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
</style>
