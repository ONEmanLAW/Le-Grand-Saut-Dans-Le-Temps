<template>
  <div class="game-rules-intro-screen" @click="handleScreenClick">
    <video
      ref="videoPlayer"
      class="video-player"
      :src="src"
      autoplay
      playsinline
      @ended="nextStep"
    ></video>
  </div>
</template>

<script>
export default {
  name: 'GameRulesIntro',
  props: {
    src: String,
    nextStep: Function
  },
  data() {
    return {
      clickCount: 0
    };
  },
  mounted() {
 

    const video = this.$refs.videoPlayer;
    video.play().catch(error => {
      console.warn("Video autoplay prevented:", error);
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
        video.pause(); 
        video.currentTime = video.duration; 
        this.nextStep(); 
        this.clickCount = 0;
      }
    }
  }
}
</script>

<style scoped>
.game-rules-intro-screen {
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
  cursor: pointer;
}

.video-player {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}
</style>