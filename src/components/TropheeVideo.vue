<template>
  <div class="trophee-video-screen">
    <video
      v-if="tropheeVideoSource"
      ref="tropheeVideoPlayer"
      :src="tropheeVideoSource"
      autoplay
      playsinline
      @ended="onTropheeVideoEnded"
    >
      Votre navigateur ne supporte pas la lecture de vidéos.
    </video>
  </div>
</template>

<script>
export default {
  props: ['totalQuestions', 'videoSources', 'nextStep'],
  data() {
    return {
      trophee: null,
      score: 0,
      questions: 0,
    }
  },
  computed: {
    tropheeVideoSource() {
      return this.trophee ? this.videoSources[this.trophee] : this.videoSources['none']
    }
  },
  mounted() {
    this.score = parseInt(localStorage.getItem('score') || '0')
    this.questions = parseInt(localStorage.getItem('questionCount') || '0')
    this.determineTrophee()
    this.$nextTick(() => {
      const player = this.$refs.tropheeVideoPlayer
      if (player) {
        player.volume = 1.0 // Assure que le volume est à fond
        player.play().catch(err => {
          console.warn('Lecture auto refusée par le navigateur :', err)
        })
      }
    })
  },
  methods: {
    determineTrophee() {
      const correctAnswers = this.score
      const questions = this.questions

      if (questions === 8) {
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
      } else if (questions === 20) {
        if (correctAnswers >= 16) this.trophee = 'or'
        else if (correctAnswers >= 13) this.trophee = 'argent'
        else if (correctAnswers >= 10) this.trophee = 'bronze'
        else this.trophee = 'none'
      } else {
        this.trophee = 'none'
      }
    },
    onTropheeVideoEnded() {
      if (typeof this.nextStep === 'function') {
        this.nextStep()
      }
    }
  }
}
</script>

<style scoped>
.trophee-video-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  background: black;
  z-index: 9999;
}

video {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  display: block;
}
</style>
