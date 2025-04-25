<template>
    <audio ref="audioElement" loop>
      <source :src="src" :type="type" />
      Votre navigateur ne prend pas en charge la balise audio.
    </audio>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const props = defineProps({
    src: String,
    type: String
  })
  
  const audioElement = ref(null)
  
  onMounted(() => {
    if (audioElement.value) {
      audioElement.value.play()
    }
  })
  </script>
  
  <style scoped>
  /* Styles pour l'audio si nécessaire */
  </style>
  