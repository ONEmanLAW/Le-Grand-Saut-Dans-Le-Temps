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
  </div>
</template>

<script>
export default {
  name: 'GenericScreen',
  props: {
    src: { type: String, required: true },
    nextStep: { type: Function, required: true }
  },
  data() {
    return {
      clickCount: 0
    };
  },
  mounted() {
    const video = this.$refs.videoPlayer;
    video.play().catch(() => {
      // This catch block often handles cases where autoplay is blocked
      // and a user interaction is needed to initiate playback.
      // We can keep it or remove it if it's not causing issues.
      video.play();
    });
  },
  methods: {
    handleScreenClick() {
      this.clickCount++;
      if (this.clickCount >= 3) {
        this.skipVideo();
      }
    },
    skipVideo() {
      const video = this.$refs.videoPlayer;
      if (video) {
        video.pause(); // Pause the video
        video.currentTime = video.duration; // Jump to the end
        this.nextStep(); // Trigger the next step
        this.clickCount = 0; // Reset click count
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