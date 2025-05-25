<template>
  <div class="end-video-screen">
    <video
      :src="src"
      autoplay
      playsinline
      @ended="onVideoEnded"
      :muted="false"
      controls="false"
    >
      Votre navigateur ne supporte pas la lecture de vidéos.
    </video>
  </div>
</template>

<script>
export default {
  props: ['src', 'nextStep'],
  methods: {
    onVideoEnded() {
      if (typeof this.nextStep === 'function') {
        this.nextStep()
      }
    }
  }
}
</script>
