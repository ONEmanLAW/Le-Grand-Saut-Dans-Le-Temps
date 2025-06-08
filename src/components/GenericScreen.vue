<template>
  <div class="video-screen" @click="handleScreenClick">
    <video
      ref="videoPlayer"
      class="video-player"
      autoplay
      playsinline
      @ended="nextStep"
    >
      <source :src="src" type="video/mp4" />
      Votre navigateur ne supporte pas la vidéo HTML5.
    </video>

    <ButtonInputListener
      :active="false"
      :onButtonPress="() => {}"
    />
  </div>
</template>

<script>
import ButtonInputListener from './ButtonInputListener.vue'

export default {
  name: 'GenericScreen',
  components: { ButtonInputListener },
  props: {
    src: { type: String, required: true },
    nextStep: { type: Function, required: true }
  },
  data() {
    return {
      clickCount: 0
    }
  },
  mounted() {
    const video = this.$refs.videoPlayer
    video.play().catch(() => {
      video.play()
    })
  },
  methods: {
    handleScreenClick() {
      this.clickCount++
      if (this.clickCount >= 3) {
        this.skipVideo()
      }
    },
    skipVideo() {
      const video = this.$refs.videoPlayer
      if (video) {
        video.pause()
        video.currentTime = video.duration
        this.nextStep()
        this.clickCount = 0
      }
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
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.video-player {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  z-index: 0;
}
</style>
