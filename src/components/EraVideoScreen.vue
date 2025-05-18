<template>
  <div class="video-screen">
    <video
      ref="videoPlayer"
      class="video-player"
      :src="currentVideo"
      autoplay
      playsinline
      @ended="nextStep"
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
      selectedEra: localStorage.getItem('selectedEra') || '50'
    }
  },
  computed: {
    currentVideo() {
      return this.videoSources?.[this.selectedEra] || ''
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
