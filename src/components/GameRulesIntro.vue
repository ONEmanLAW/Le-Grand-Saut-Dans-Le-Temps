<template>
  <div class="game-rules-intro-screen">
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
}

.video-player {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  display: block;
}
</style>
