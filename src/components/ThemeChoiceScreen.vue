<template>
  <div class="screen">
    <!-- Choisir votre thème avec une bordure noire -->
    <h1 class="choose-theme-title">Choisissez un thème</h1>
    
    <div class="themes">
      <!-- Premier bouton avec fond rouge -->
      <button 
        v-for="(theme, index) in shuffledThemes" 
        :key="theme" 
        @click="select(theme)" 
        :class="index === 0 ? 'theme-button-red' : 'theme-button-blue'"
      >
        {{ theme }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['themeSelected'])
const allThemes = ['Musique', 'Histoire',]
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

.screen {
  text-align: center;
  padding: 20px;
}

.choose-theme-title {
  font-weight: bold;
  border: 2px solid black;
  border-radius: 10px;
  background-color: white;
  padding: 10px;
  display: inline-block;
  color: black;
  margin-bottom: 40px;
}

.themes {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-top: 150px;
  align-items: center;
}

button {
  font-size: 48px;
  width: 70%;
  padding: 30px 45px;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.2s;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); 
}

.theme-button-red {
  background-color: red;
}

.theme-button-red:hover {
  background-color: darkred;
}


.theme-button-blue {
  background-color: blue;
}

.theme-button-blue:hover {
  background-color: darkblue;
}
</style>
