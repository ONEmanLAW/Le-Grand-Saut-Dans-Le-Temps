<template>
    <div class="score-screen">
      <h1 class="title">🎉 Fin de la partie !</h1>
      <p class="score">Votre score : <strong>{{ score }}/{{ total }}</strong></p>
  
      <div v-if="score === total" class="score-message">
        <h2>💯 Parfait ! Bravo !</h2>
      </div>
      <div v-else-if="score / total >= 0.75">
        <h2>👏 Très bon score !</h2>
      </div>
      <div v-else-if="score / total >= 0.5">
        <h2>👍 Pas mal !</h2>
      </div>
      <div v-else>
        <h2>🤔 Ce n'est qu'un jeu, réessaie !</h2>
      </div>
  
      <button @click="$emit('restart')">🔁 Rejouer</button>
    </div>
  </template>
  
  <script setup>
  defineProps({
    score: Number,
    total: Number
  })
  
  defineEmits(['restart'])
  </script>
  
  <style scoped>
  .score-screen {
    text-align: center;
    padding: 2rem;
    font-family: 'Open Sans', sans-serif;
    color: black;
  }

  .score {
    font-size: 38px;
  }
  
  button {
    margin-top: 2rem;
    padding: 1rem 2rem;
    font-size: 1.2rem;
    cursor: pointer;
    background-color: #222;
    color: white;
    border: none;
    border-radius: 8px;
  }
  </style>
  