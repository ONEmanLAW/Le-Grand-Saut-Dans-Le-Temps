<template>
  <div class="theme-intro-video-screen">
    <video
      ref="videoPlayer"
      class="video-player"
      :src="currentVideo"
      autoplay
      playsinline
      @ended="nextStep"
      @click="handleClick"
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
      selectedTheme: localStorage.getItem("selectedTheme") || "",
      clickCount: 0,
      clickTimeout: null,
    };
  },
  computed: {
    currentVideo() {
      return this.videoSources?.[this.selectedTheme] || "";
    }
  },
  methods: {
    handleClick() {
      this.clickCount++;

      // Si 3 clics atteints, on skip la vidéo
      if (this.clickCount >= 3) {
        this.nextStep();
        this.resetClicks();
        return;
      }

      // Reset le compteur si pas 3 clics en moins de 1 seconde
      clearTimeout(this.clickTimeout);
      this.clickTimeout = setTimeout(() => {
        this.resetClicks();
      }, 1000);
    },
    resetClicks() {
      this.clickCount = 0;
      clearTimeout(this.clickTimeout);
      this.clickTimeout = null;
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
