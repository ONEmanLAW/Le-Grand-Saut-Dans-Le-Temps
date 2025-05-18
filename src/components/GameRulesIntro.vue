<template>
  <div class="video-screen">
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
    nextStep: Function,
    src: String
  }
}
</script>
