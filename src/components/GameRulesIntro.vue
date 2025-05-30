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
      clickCount: 0 // Initialize click counter
    };
  },
  mounted() {
    // You might still want this if autoplay is sometimes blocked,
    // though the playsinline and autoplay attributes generally handle most cases.
    const video = this.$refs.videoPlayer;
    video.play().catch(error => {
      console.warn("Video autoplay prevented:", error);
      // Fallback or user prompt to play video could go here
    });
  },
  methods: {
    /**
     * Handles clicks on the screen to enable a debug skip feature.
     * After 3 clicks, the video will be skipped.
     */
    handleScreenClick() {
      this.clickCount++;
      if (this.clickCount >= 3) {
        this.skipVideo();
      }
    },
    /**
     * Skips the current video by pausing it, jumping to the end,
     * and triggering the next step in the application flow.
     */
    skipVideo() {
      const video = this.$refs.videoPlayer;
      if (video) {
        video.pause(); // Stop playback
        video.currentTime = video.duration; // Jump to the end of the video
        this.nextStep(); // Call the nextStep prop to advance
        this.clickCount = 0; // Reset the click count for future use
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
  /* Make sure this div is on top and clickable */
  cursor: pointer; /* Give a visual cue that it's interactive */
}

.video-player {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  display: block;
  /* Position the video relative to its parent .game-rules-intro-screen
     to ensure the click handler on the parent is effective. */
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1; /* Place the video behind the clickable area if needed */
}
</style>