<template>
    <div class="screen">
      <h1>Choisissez un thème</h1>
      <div class="themes">
        <button v-for="theme in shuffledThemes" :key="theme" @click="select(theme)">
          {{ theme }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const emit = defineEmits(['themeSelected'])
  const allThemes = ['Musique', 'Politique', 'Animaux', 'Sport']
  const shuffledThemes = ref([])
  
  onMounted(() => {
    const random = [...allThemes].sort(() => Math.random() - 0.5)
    shuffledThemes.value = random.slice(0, 2)
  })
  
  function select(theme) {
    emit('themeSelected', theme)
  }
  </script>
  
  <style scoped>
  .themes {
    display: flex;
    gap: 20px;
    margin-top: 40px;
  }
  button {
    font-size: 1.5rem;
    padding: 10px 30px;
    background-color: #444;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.2s;
  }
  button:hover {
    background-color: #666;
  }
  </style>
  