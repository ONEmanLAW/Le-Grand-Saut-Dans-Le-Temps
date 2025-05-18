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
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.video-player {
  max-width: 100%;
  max-height: 100%;
}
</style>
