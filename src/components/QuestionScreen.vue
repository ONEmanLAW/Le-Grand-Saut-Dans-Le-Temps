<script>
import ButtonInputListener from './ButtonInputListener.vue'

export default {
  components: { ButtonInputListener },
  props: ['flowObject', 'nextStep'],
  data() {
    return {
      questionsData: null,
      beforeAudioProgress: 0,
      beforeAudioDuration: 0,

      currentQuestionIndexInLevel: 0,
      currentDifficultyIndex: 0,
      progressPercent: 0,
      difficulties: ['easy', 'medium', 'hard', 'expert'],
      transitionVideos: {
        medium: {
          bien: '/videos/facile_bien.mp4',
          pasBien: '/videos/facile_pasBien.mp4',
        },
        hard: {
          bien: '/videos/medium_bien.mp4',
          pasBien: '/videos/medium_pasBien.mp4',
        },
        expert: {
          bien: '/videos/hard_bien.mp4',
          pasBien: '/videos/hard_pasBien.mp4',
        }
      },
      endVideos: {
        bien: '/videos/expert_bien.mp4',
        pasBien: '/videos/expert_pasBien.mp4',
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
      answerColors: ['#47DEB1', '#FF8FC3', '#F16565', '#A695FF'],
      isBeforeQuestion: false,
      isFeedback: false,
      gameFinished: false,
      awaitFullTrackChoice: false,
      playingFullTrack: false,
      score: 0,
      levelScores: {
        easy: 0,
        medium: 0,
        hard: 0,
        expert: 0
      },
      isEndVideoPlaying: false,
      buttonsEnabled: false, 

      showCountdownBeforeMedia: false,
      countdownPhase: null,
      countdownValue: 3,
    };
  },
  async mounted() {
    const era = localStorage.getItem('selectedEra');
    this.currentTheme = localStorage.getItem('selectedTheme');
    this.totalQuestionsToAsk = parseInt(localStorage.getItem('questionCount') || '0');
    let questionsFile = era === '80' ? '/data/questions_80.json' : '/data/questions_50.json';

    if (this.currentTheme && this.totalQuestionsToAsk > 0) {
      this.questionsPerLevel = Math.floor(this.totalQuestionsToAsk / this.difficulties.length);
      try {
        const response = await fetch(questionsFile);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        this.questionsData = await response.json();
        this.startNextQuestionCycle();
        this.loading = false;
      } catch (e) {
        this.error = e;
        this.loading = false;
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
    },
    dynamicAnswerColors() {
      const count = this.currentQuestion?.answers?.length || 0;
      return count === 2
        ? ['#47DEB1', '#F16565']
        : ['#47DEB1', '#FF8FC3', '#F16565', '#A695FF'];
    }
  },
  methods: {
    startNextQuestionCycle() {
      this.isFeedback = false;
      this.prepareQuestionDisplay();
    },
    stopQuestionAudio() {
      const audioElement = this.$refs.questionAudio;
      if (audioElement && !audioElement.paused) {
        audioElement.pause();
        audioElement.currentTime = 0;
      }
    },
    updateProgress() {
      const audio = this.$refs.fullTrackAudio;
      if (audio && audio.duration) {
        this.progressPercent = (audio.currentTime / audio.duration) * 100;
      }
    },
    initBeforeAudioDuration() {
      const audio = this.$refs.beforeQuestionAudio;
      if (audio) {
        this.beforeAudioDuration = audio.duration;
      }
    },

    updateBeforeAudioProgress() {
      const audio = this.$refs.beforeQuestionAudio;
      if (audio && this.beforeAudioDuration) {
        this.beforeAudioProgress = (audio.currentTime / this.beforeAudioDuration) * 100;
      }
    },

    prepareQuestionDisplay() {
      this.preparingQuestion = true;
      this.questionNumberDisplay = `QUESTION ${this.totalQuestionsAsked + 1} / ${this.totalQuestionsToAsk}`;
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

        this.showCountdownBeforeMedia = true;
        this.countdownPhase = 'attention';

        setTimeout(() => {
          this.countdownPhase = 'countdown';
          this.countdownValue = 3;

          const countdownInterval = setInterval(() => {
            this.countdownValue--;

            if (this.countdownValue === 0) {
              clearInterval(countdownInterval);
              this.showCountdownBeforeMedia = false;
              this.countdownPhase = null;

              this.$nextTick(() => {
                const video = this.$refs.beforeQuestionVideo;
                const audio = this.$refs.beforeQuestionAudio;

                if (video) {
                  video.play().catch(e => {
                    console.warn("Lecture auto vidéo bloquée :", e);
                  });
                } else if (audio) {
                  audio.play().catch(e => {
                    console.warn("Lecture auto audio bloquée :", e);
                  });
                }
              });
            }
          }, 1000);

        }, 1000);
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

      if (this.$refs.beforeQuestionVideo) {
        this.$refs.beforeQuestionVideo.pause();
        this.$refs.beforeQuestionVideo.currentTime = 0;
        this.$refs.beforeQuestionVideo.muted = false;
        this.$refs.beforeQuestionVideo.play();
      }
    },

    loadQuestion() {
      clearTimeout(this.timeoutId);
      this.transitionVideo = false;
      this.isEndVideoPlaying = false;

      if (this.currentQuestionIndexInLevel < this.questionsPerLevel && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        const questions = this.questionsInCurrentDifficulty;
        const index = this.currentQuestionIndexInLevel % questions.length;
        this.currentQuestion = questions[index];
        this.selectedAnswer = null;
        this.answered = false;
        this.buttonsEnabled = true;

        if (this.$refs.beforeQuestionAudio) {
          this.$refs.beforeQuestionAudio.pause();
          this.$refs.beforeQuestionAudio.currentTime = 0;
        }
        if (this.$refs.beforeQuestionVideo) {
          this.$refs.beforeQuestionVideo.pause();
          this.$refs.beforeQuestionVideo.currentTime = 0;
        }

        this.$nextTick(() => {
          const audioElement = this.$refs.questionAudio;
          if (audioElement && this.currentQuestion.audio) {
            audioElement.currentTime = 0;
            audioElement.play().catch(e => {
              console.warn('Lecture audio question bloquée :', e);
            });
          }
        });
      } else {
        this.startTransitionOrEnd();
      }
    },


    selectAnswer(index) {
      if (!this.answered && this.currentQuestion && this.totalQuestionsAsked < this.totalQuestionsToAsk) {
        this.stopQuestionAudio();
        this.buttonsEnabled = false;
        this.selectedAnswer = index;
        this.answered = true;

        const isCorrect = index === this.currentQuestion.correctIndex;


        if (isCorrect) {
          this.score++;
          this.levelScores[this.currentDifficulty]++;
          this.$refs.correctSound?.play();
        } else {
          this.$refs.wrongSound?.play();
        }

        this.feedback = isCorrect
          ? 'Correct !'
          : `Incorrect. La bonne réponse était : ${this.currentQuestion.answers[this.currentQuestion.correctIndex]}`;

        this.timeoutId = setTimeout(() => {
          this.isFeedback = true;

          if (!this.currentQuestion.feedback?.audio) {
            setTimeout(() => {
              this.nextStepAfterFeedback();
            }, 6000);
          }

        }, 3000);
      }
    },

    onFullTrackChoice(yes) {
      this.awaitFullTrackChoice = false;
      if (yes) {
        this.playingFullTrack = true;
        this.buttonsEnabled = true;  
        this.$nextTick(() => {
          this.$refs.fullTrackAudio.play().catch(e => {
            console.warn("Lecture fullTrack bloquée", e);
          });
        });
      } else {
        this.totalQuestionsAsked++;
        this.moveToNextStep();
      }
    },

    skipFullTrack() {
      if (!this.playingFullTrack) return;
      this.$refs.fullTrackAudio.pause();
      this.$refs.fullTrackAudio.currentTime = 0;
      this.playingFullTrack = false;
      this.totalQuestionsAsked++;
      this.moveToNextStep();
    },

    onFullTrackEnded() {
      this.playingFullTrack = false;
      this.totalQuestionsAsked++;
      this.moveToNextStep();
    },



    handleButtonPress(buttonId) {
 
      if (this.awaitFullTrackChoice) {
        if (buttonId === 'A') {
          this.onFullTrackChoice(true); 
        } else if (buttonId === 'C') {
          this.onFullTrackChoice(false); 
        }
        return;
      }

    
      if (this.playingFullTrack) {
        this.skipFullTrack();
        return;
      }

      
      if (!this.buttonsEnabled || !this.currentQuestion?.answers) return;

      const answerCount = this.currentQuestion.answers.length;

      let index;

      if (answerCount === 2) {
        const map = { A: 0, C: 1 };
        index = map[buttonId];
      } else {
        const map = { A: 0, B: 1, C: 2, D: 3 };
        index = map[buttonId];
      }

      if (index !== undefined) {
        this.selectAnswer(index);
      }
    },

    nextStepAfterFeedback() {
      this.isFeedback = false;

      // je te déteste IOS /// 
      const fullTrack = this.currentQuestion?.fullTrack;
      if (fullTrack) {
        this.awaitFullTrackChoice = true;
        this.buttonsEnabled = false;      
      } else {
        this.totalQuestionsAsked++;
        if (this.totalQuestionsAsked >= this.totalQuestionsToAsk) {
          this.playEndVideo();
        } else {
          this.moveToNextStep();
        }
      }
    },
    moveToNextStep() {
      this.currentQuestionIndexInLevel++;
      if (this.currentQuestionIndexInLevel < this.questionsPerLevel) {
        this.startNextQuestionCycle();
      } else {
        this.startTransitionOrEnd();
      }
    },
    startTransitionOrEnd() {
      if (this.currentDifficulty === 'expert') {
        this.playEndVideo();
        return;
      }

      const nextDifficulty = this.difficulties[this.currentDifficultyIndex + 1];

      if (
        this.currentDifficultyIndex < this.difficulties.length - 1 &&
        this.totalQuestionsAsked < this.totalQuestionsToAsk
      ) {
        this.transitionVideo = true;

        const seuilMoyen = Math.ceil(this.questionsPerLevel / 2);
        const scoreNiveauPrecedent = this.levelScores[this.currentDifficulty];

        this.transitionVideoSource =
          scoreNiveauPrecedent >= seuilMoyen
            ? this.transitionVideos[nextDifficulty]?.bien
            : this.transitionVideos[nextDifficulty]?.pasBien;

        this.$nextTick(() => {
          const video = this.$refs.transitionVideoPlayer;
          if (video && this.transitionVideoSource) {
            video.muted = false; 
            video.play().catch((e) => {
              console.warn('Lecture vidéo bloquée :', e);
            });
          } else {
            this.nextLevel();
          }
        });
      } else {
        this.playEndVideo();
      }
    },

    nextLevel() {
      this.currentDifficultyIndex++;
      this.currentQuestionIndexInLevel = 0;
      this.startNextQuestionCycle();
    },
    playEndVideo() {
      this.transitionVideo = true;
      this.isEndVideoPlaying = true;

      const seuilMoyen = Math.ceil(this.questionsPerLevel / 2);
      const scoreExpert = this.levelScores.expert;

      this.transitionVideoSource =
        scoreExpert >= seuilMoyen ? this.endVideos.bien : this.endVideos.pasBien;

      this.$nextTick(() => {
        if (this.$refs.transitionVideoPlayer && this.transitionVideoSource) {
          this.$refs.transitionVideoPlayer.play();
        } else {
          this.finishGame();
        }
      });
    },
    onTransitionVideoEnded() {
      if (this.isEndVideoPlaying) {
        this.isEndVideoPlaying = false;
        this.finishGame();
      } else {
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
      if (this.nextStep) {
        this.nextStep();
      }
    }
  }
};
</script>

<template>
  <audio ref="correctSound" src="/audio/correctSound.mp3" preload="auto"></audio>
  <audio ref="wrongSound" src="/audio/wrongSound.mp3" preload="auto"></audio>

  <audio ref="questionAudio" :src="currentQuestion?.audio || ''" preload="auto"></audio>



    <div v-if="awaitFullTrackChoice" class="fulltrack-choice-screen">
      <p>Voulez-vous écouter la musique entièrement ?</p>
      <div class="button-row">
        <div class="button-wrapper">
          <button class="yes" @click="onFullTrackChoice(true)">Oui</button>
        </div>
        <div class="button-wrapper">
          <button class="no" @click="onFullTrackChoice(false)">Non</button>
        </div>
      </div>
    </div>


  <div v-if="playingFullTrack" class="fulltrack-player-screen" @click="skipFullTrack">
    <audio
      ref="fullTrackAudio"
      :src="currentQuestion.fullTrack"
      @ended="onFullTrackEnded"
      @timeupdate="updateProgress"
      autoplay
    ></audio>

    <div class="progress-bar-container">
      <div class="progress-bar">
        <div class="progress-circle" :style="{ left: progressPercent + '%' }"></div>
      </div>
    </div>

    <p>Cliquez sur un bouton ou sur l'écran pour passer la musique</p>
  </div>



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
        <h1 class="questionTextNumber">{{ questionNumberDisplay }}</h1>
      </div>
    </div>

    <div v-if="transitionVideo && transitionVideoSource">
      <video
        ref="transitionVideoPlayer"
        :src="transitionVideoSource"
        autoplay
        playsinline
        class="transition-video"
        @ended="onTransitionVideoEnded"
        
      ></video>
    </div>

    <div v-else-if="isBeforeQuestion && currentQuestion?.beforeQuestion">
      <div class="before-question-content">
        <h2 v-if="currentQuestion.beforeQuestion.text">{{ currentQuestion.beforeQuestion.text }}</h2>

        <div v-if="showCountdownBeforeMedia" class="countdown-overlay">
          <div class="countdown-text">
            <template v-if="countdownPhase === 'attention'">
              Attention
            </template>
            <template v-else-if="countdownPhase === 'countdown'">
              {{ countdownValue }}
            </template>
          </div>
        </div>

        <!-- Soit l'audio soit la video -->
        <video
            v-if="currentQuestion.beforeQuestion.video"
          ref="beforeQuestionVideo"
          :src="currentQuestion.beforeQuestion.video"
          playsinline
          @ended="startQuestion"
          class="before-question-video"
        ></video>


        <audio
          v-else-if="currentQuestion.beforeQuestion.audio"
          ref="beforeQuestionAudio"
          :src="currentQuestion.beforeQuestion.audio"
          @ended="startQuestion"
          @timeupdate="updateBeforeAudioProgress"
          @loadedmetadata="initBeforeAudioDuration"
          playsinline
        ></audio>
        

      <div v-if="currentQuestion.beforeQuestion.audio" class="progress-bar-container">
        <div class="progress-bar">
          <div
            class="progress-circle"
            :style="{ left: beforeAudioProgress + '%' }"
          ></div>
        </div>
      </div>


      </div>
    </div>

    <div v-else-if="isFeedback && currentQuestion?.feedback">
      <div class="feedback-content">
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


    <div v-else-if="currentQuestion" class="question-screen">
      <h2>{{ currentQuestion.question }}</h2>
      <ul class="answers-grid" :data-count="currentQuestion.answers.length">
       <li
          v-for="(answer, index) in currentQuestion.answers"
          :key="index"
          :class="{
            correct: answered && index === currentQuestion.correctIndex,
            faded: answered && index !== currentQuestion.correctIndex
          }"
        >
          <button
            @click="selectAnswer(index)"
            :disabled="answered"
            :style="{ backgroundColor: dynamicAnswerColors[index % dynamicAnswerColors.length] }"
          >
            {{ answer }}
          </button>
        </li>
      </ul>
    </div>

    <div v-else>
      <p>{{ feedback || 'Fin de la partie !' }}</p>
    </div>

    <!--Pour boutton -->
    <ButtonInputListener
      :active="buttonsEnabled || awaitFullTrackChoice"
      :onButtonPress="handleButtonPress"
    />
  </div>
</template>





<style scoped>



.question-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 50px 20px;
  font-family: 'Arial', sans-serif;
  text-align: center;
  background: transparent;
  box-shadow: none;
  border: none;
}

.question-screen h2 {
  font-weight: bold;
  margin-top: 0;
  margin-bottom: 70px;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 1.2s ease-out forwards;
}


.answers-grid {
  list-style: none;
  padding: 0;
  margin: 0 auto;
  display: grid;
  justify-content: center;
  gap: 40px;
  overflow: visible;
}

/*
 2 réponses = 1 colonne
*/
.answers-grid[data-count="2"] {
  grid-template-columns: 1fr;
}

/*
 3 ou 4 réponses = 2 colonnes
*/
.answers-grid[data-count="3"],
.answers-grid[data-count="4"] {
  grid-template-columns: repeat(2, 1fr);
  gap: 40px 60px;
}

.answers-grid li {
  display: flex;
  justify-content: center;
  width: auto;
  position: relative;
  overflow: visible;
}

.answers-grid li.correct button {
  opacity: 1;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.answers-grid li.faded button {
  opacity: 0.3;
  pointer-events: none;
  transition: opacity 0.3s ease;
}


.answers-grid button {
  width: 560px;
  height: 225px;
  font-size: 48px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  border-radius: 16px;
  background-color: white;
  color: black;
  transition: filter 0.3s ease, opacity 0.3s ease;
  position: relative;
  z-index: 1;
  opacity: 0;
  animation: fadeInUp 1.2s ease-out forwards;

  box-shadow: 0px 8px 10px rgba(0, 0, 0, 1);
}

/* 
2 réponses = version très large
 */
.answers-grid[data-count="2"] button {
  width: 1160px;
  height: 225px;
}


.answers-grid button:hover:not(:disabled) {
  filter: brightness(85%);
}


.answers-grid button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* États correct/incorrect */
/* .answers-grid li.correct button {
  border: 3px solid #28a745;
  color: #28a745;
}

.answers-grid li.incorrect button {
  border: 3px solid #dc3545;
  color: #dc3545;
} */



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


/* .question-screen.answered-state .answers-grid li:not(.correct) {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
} */

.faded {
  opacity: 0.4;
  pointer-events: none;
  transition: opacity 0.3s ease;
}



.fullscreen-message {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #FFAE59;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  color: #330006;
  font-size: 55px;
  font-weight: bold;
  font-family: 'Berlin', sans-serif;
}

.questionTextNumber {
  border-top: 6px solid #330006;
  border-bottom: 6px solid #330006;
  border-left: none;
  border-right: none;
  text-transform: uppercase;
  font-size: 72px;
}


.before-question-content {
  display: flex;
  flex-direction: column;
  height: 100vh;
  box-sizing: border-box;
  padding: 20px;
}

.before-question-content h2 {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
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

.before-question-video {

  width: 100%;
  height: 85%;
  border-radius: 8px;
  object-fit: contain;
}

.feedback-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px; 
  padding: 20px;
}

.feedback-content h2 {
  margin-bottom: 20px;
}

.feedback-content img.feedback-image {
  max-width: 80vw;
  max-height: 60vh;  
  width: auto;          
  height: auto;    
  border-radius: 8px;
  display: block;
  margin: 0 auto;
}


.feedback-content p.feedback-text {
  text-align: center;
  max-width: 600px;
  margin-top: 40px;
  font-weight: bold;
}

.feedback-content audio {
  margin-bottom: 20px;
}

.countdown-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #FFAE59;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.countdown-text {
  font-size: 72px;
  color: #330006;
  font-weight: bold;
  user-select: none;
  text-align: center;
  font-family: 'Berlin', sans-serif;
}

.transition-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  z-index: 9999;
}



.fulltrack-choice-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 70px;
  box-sizing: border-box;
  color: white;
  overflow: hidden;
  font-family: 'Berlin', sans-serif;
}

.fulltrack-choice-screen p {
  font-weight: bold;
  margin-bottom: 40px;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 1.2s ease-out forwards;
  width: 800px;
  font-size: 55px;
  font-family: 'Berlin', sans-serif;
}


.fulltrack-choice-screen .button-row {
  display: flex;
  flex-direction: column;
  gap: 40px;
  justify-content: center;
  align-items: center;
  overflow: visible;
}

.fulltrack-choice-screen .button-wrapper {
  overflow: visible;
  margin-bottom: 40px;
  position: relative;
  width: 1160px;
}


.fulltrack-choice-screen button {
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
  font-family: 'Berlin', sans-serif;
}


.fulltrack-choice-screen button.yes {
  background-color: #47DEB1;
  font-size: 55px;
  font-family: 'NeutraText', sans-serif;
}


.fulltrack-choice-screen button.no {
  background-color: #F16565;
  font-size: 55px;
  font-family: 'NeutraText', sans-serif;
}

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

.fulltrack-player-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 40px;
  box-sizing: border-box;
  color: white;
  text-align: center;
  width: 100%;
}

.fulltrack-player-screen audio {
  display: none;
}

.progress-bar-container {
  background-color: #FFAE59;
  padding: 25px 40px;
  border-radius: 12px;
  width: 80%;
  max-width: 1000px;
  margin: 30px auto;
  box-sizing: border-box;


  opacity: 0;
  animation: fadeInUp 1s ease-out forwards;
}

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
.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #330006;
  border-radius: 3px;
  position: relative;

  overflow: visible;
}

.progress-circle {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 22px;
  height: 22px;
  background-color: #330006;
  border-radius: 50%;
  transition: left 0.1s linear;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}






</style>
