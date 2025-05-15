<template>
  <div class="video-screen">
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
  </div>
</template>

<script>
export default {
  name: 'GenericScreen',
  props: {
    src: { type: String, required: true },
    nextStep: { type: Function, required: true }
  },
  mounted() {
    const video = this.$refs.videoPlayer
    video.play().catch(() => {
      video.play()
    })
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
}

.video-player {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover;
}
</style>

