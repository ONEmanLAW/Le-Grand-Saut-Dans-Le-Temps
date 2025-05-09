<template>
    <div id="video-container">
      <video id="video-element" ref="video" autoplay @ended="handleEnded">
        <source src="/videos/video1.mp4" type="video/mp4" />
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
    display: flex;
    justify-content: center;
    align-items: center;
  }
  #video-element {
    width: 100%;
    max-width: 800px;
  }
  </style>
  