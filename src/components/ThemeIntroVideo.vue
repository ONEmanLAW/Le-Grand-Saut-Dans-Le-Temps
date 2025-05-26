<template>
  <div class="theme-intro-video-screen">
    <video
      ref="videoPlayer"
      class="video-player"
      :src="currentVideo"
      autoplay
      playsinline
      @ended="nextStep"
      muted="false"
    ></video>
  </div>
</template>

<script>
export default {
  name: "ThemeIntroVideo",
  props: {
    nextStep: Function,
    videoSources: Object
  },
  data() {
    return {
      selectedTheme: localStorage.getItem("selectedTheme") || ""
    };
  },
  computed: {
    currentVideo() {
      return this.videoSources?.[this.selectedTheme] || "";
    }
  }
};
</script>

<style scoped>
.theme-intro-video-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  background: black;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.video-player {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
}
</style>
