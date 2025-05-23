<template>
  <div class="trophee-video-screen">
    <h2 v-if="trophee">{{ getTropheeTitle }} !</h2>
    <p v-else>Fin de la partie.</p>
    <video v-if="tropheeVideoSource" ref="tropheeVideoPlayer" :src="tropheeVideoSource" autoplay muted playsinline>
      Votre navigateur ne supporte pas la lecture de vidéos.
    </video>
  </div>
</template>

<script>
export default {
  props: ['totalQuestions', 'videoSources'], // on enlève 'score' ici
  data() {
    return {
      trophee: null,
      score: 0,  // ajout d’une donnée score locale
      questions: 0
    };
  },
  computed: {
    tropheeVideoSource() {
      return this.trophee ? this.videoSources[this.trophee] : this.videoSources['none'];
    },
    getTropheeTitle() {
      if (this.trophee === 'or') return "Trophée d'or";
      if (this.trophee === 'argent') return "Trophée d'argent";
      if (this.trophee === 'bronze') return "Trophée de bronze";
      return "";
    }
  },
  mounted() {
    // Récupération score et nombre questions dans localStorage
    this.score = parseInt(localStorage.getItem('score') || '0');
    this.questions = parseInt(localStorage.getItem('questionCount') || '0');
    this.determineTrophee();
  },
  methods: {
    determineTrophee() {
      const correctAnswers = this.score;
      const questions = this.questions;

      if (questions === 8) {
        if (correctAnswers >= 7) this.trophee = 'or';
        else if (correctAnswers >= 5) this.trophee = 'argent';
        else if (correctAnswers >= 4) this.trophee = 'bronze';
        else this.trophee = 'none';
      } else if (questions === 12) {
        if (correctAnswers >= 10) this.trophee = 'or';
        else if (correctAnswers >= 8) this.trophee = 'argent';
        else if (correctAnswers >= 6) this.trophee = 'bronze';
        else this.trophee = 'none';
      } else if (questions === 16) {
        if (correctAnswers >= 13) this.trophee = 'or';
        else if (correctAnswers >= 10) this.trophee = 'argent';
        else if (correctAnswers >= 8) this.trophee = 'bronze';
        else this.trophee = 'none';
      } else if (questions === 20) {
        if (correctAnswers >= 16) this.trophee = 'or';
        else if (correctAnswers >= 13) this.trophee = 'argent';
        else if (correctAnswers >= 10) this.trophee = 'bronze';
        else this.trophee = 'none';
      } else {
        this.trophee = 'none';
      }
    }
  }
};
</script>

<style scoped>
.trophee-video-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 40px;
  font-family: 'Arial', sans-serif;
  background-color: #f0f0f0;
}

h2 {
  color: gold;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
  color: #555;
  margin-bottom: 20px;
}

video {
  max-width: 80%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>