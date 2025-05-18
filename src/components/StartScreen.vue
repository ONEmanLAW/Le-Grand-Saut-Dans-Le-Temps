<template>
  <div class="start-screen" @click="handleClick">
    <img :src="src" alt="Start Screen" class="full-image" />
  </div>
</template>

<script>
export default {
  name: 'StartScreen',
  props: {
    src: { type: String, required: true },
    nextStep: { type: Function, required: true }
  },
  methods: {
    handleClick() {
      const elem = this.$el

      if (elem.requestFullscreen) {
        elem.requestFullscreen()
          .then(() => {
            // Fullscreen lancé, on passe à l'étape suivante
            this.nextStep()
          })
          .catch(err => {
            console.warn('Erreur fullscreen:', err)
            // Même en cas d’erreur, on continue
            this.nextStep()
          })
      } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen()
        this.nextStep()
      } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen()
        this.nextStep()
      } else {
        // Pas supporté, on continue quand même
        this.nextStep()
      }
    }
  }
}
</script>

<style scoped>
.start-screen {
  overflow: hidden;
  height: 100vh;
  width: 100vw;
  cursor: pointer;
}

.full-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
</style>
