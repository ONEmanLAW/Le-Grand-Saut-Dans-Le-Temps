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

<style>
.end-video-screen {
  position: fixed; /* Pour recouvrir toute la fenêtre */
  top: 0;
  left: 0;
  width: 100vw; /* Largeur de la fenêtre */
  height: 100vh; /* Hauteur de la fenêtre */
  display: flex;
  justify-content: center; /* Centrer horizontalement */
  align-items: center; /* Centrer verticalement */
  z-index: 9999; /* Pour s'assurer qu'il est au-dessus des autres éléments */
}

.end-video-screen video {
  display: block; /* Empêche un espace en bas de la vidéo */
  max-width: 100%; /* S'assure que la vidéo ne dépasse pas la largeur */
  max-height: 100%; /* S'assure que la vidéo ne dépasse pas la hauteur */
}
</style>