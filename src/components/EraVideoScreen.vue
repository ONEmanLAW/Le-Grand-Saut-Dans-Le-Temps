<template>
  <div class="video-screen">
    <video
      ref="videoPlayer"
      class="video-player"
      :src="currentVideo"
      autoplay
      playsinline
      @ended="handleEnded"
    ></video>
  </div>
</template>

<script>
export default {
  name: 'EraVideoScreen',
  props: {
    nextStep: Function,
    videoSources: Object
  },
  data() {
    return {
      // Ne pas forcer la valeur '50' ici pour ne pas déclencher le fond automatique
      selectedEra: localStorage.getItem('selectedEra') || null
    }
  },
  computed: {
    currentVideo() {
      return this.videoSources?.[this.selectedEra] || ''
    }
  },
  methods: {
    handleEnded() {
      if (this.selectedEra) {
        this.$emit('era-selected', this.selectedEra)
        if (typeof this.nextStep === 'function') {
          this.nextStep()
        }
      }
      // Si selectedEra est null, ne rien faire (pas de choix, pas d’émission)
    }
  }
}
</script>

<style scoped>
.video-screen {
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.video-player {
  max-width: 100%;
  max-height: 100%;
  display: block;
}
</style>
