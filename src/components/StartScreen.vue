<template>
  <div class="start-screen" @click="nextStep">
    <img :src="src" alt="Start Screen" class="full-image" />
  </div>
</template>

<script>
export default {
  name: 'StartScreen',
  props: {
    src: { type: String, required: true },
    nextStep: { type: Function, required: true }
  }
}
</script>

<style scoped>
.start-screen {
  overflow: hidden;
}

.full-image {
  width: 100%;
  object-fit: cover;
  display: block;
}
</style>
