<template>
  <div class="video-screen">
    <video
      ref="videoPlayer"
      class="video-player"
      :src="currentVideo"
      autoplay
      playsinline
      muted
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
    }
  }
}
</script>

<style scoped>
.video-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  z-index: 9999;
  background: black;
}

.video-player {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  display: block;
}
</style>
