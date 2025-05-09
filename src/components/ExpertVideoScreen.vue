<template>
    <div id="video-container">
      <video
        id="video-element"
        ref="video"
        :autoplay="false"
        @ended="handleEnded"
        @canplay="autoPlayOnceReady"
      >
        <source src="/videos/expert.mp4" type="video/mp4" />
      </video>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const video = ref(null)
  const emit = defineEmits(['ended'])
  const hasPlayed = ref(false)
  
  function play() {
    if (!hasPlayed.value && video.value) {
      hasPlayed.value = true
      video.value.play()
    }
  }
  
  function reset() {
    if (video.value) {
      video.value.pause()
      video.value.currentTime = 0
      hasPlayed.value = false
    }
  }
  
  function handleEnded() {
    emit('ended')
  }
  
  function autoPlayOnceReady() {
    if (hasPlayed.value) return
    video.value?.play()
    hasPlayed.value = true
  }
  
  defineExpose({ play, reset })
  </script>
  
  <style scoped>
  #video-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  #video-element {
    width: 100%;
    max-width: 800px;
  }
  </style>
  