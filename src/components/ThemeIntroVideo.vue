<template>
  <div class="theme-intro-video-screen">
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
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  padding: 0;
}

.video-player {
  max-width: 100%;
  max-height: 100%;
  display: block;
}
</style>
