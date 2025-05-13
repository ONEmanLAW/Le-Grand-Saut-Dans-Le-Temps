<template>
  <div id="video-container">
    <video id="video-element" ref="video" autoplay @ended="handleEnded">
      <source src="/videos/video.mp4" type="video/mp4" />
    </video>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const video = ref(null)
const emit = defineEmits(['ended'])

function play() {
  video.value?.play()
}

function reset() {
  video.value?.pause()
  video.value.currentTime = 0
}

function handleEnded() {
  emit('ended')
}

defineExpose({ play, reset })
</script>

<style scoped>
#video-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  z-index: 9999;
  display: flex;
    justify-content: center;
    align-items: center;
}

#video-element {
  width: 100%;
  max-width: 800px;
}
</style>
