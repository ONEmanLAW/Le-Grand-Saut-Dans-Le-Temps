<!-- src/components/EndVideo.vue -->
<template>
    <div class="end-video">
      <video
        ref="videoRef"
        class="video-player"
        :src="videoSrc"
        autoplay
        @ended="handleVideoEnd"
      ></video>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const emit = defineEmits(['videoEnded'])
  
  const videoRef = ref(null)
  const videoSrc = '/videos/endVideo.mp4'
  function handleVideoEnd() {
    emit('videoEnded')
  }
  
  onMounted(() => {
    videoRef.value?.play()
  })
  </script>
  
  <style scoped>
  .end-video {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: black;
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .video-player {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  </style>
  