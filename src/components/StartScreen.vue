<template>
  <div id="start-container">
    <div id="logo" @click="$emit('start')"></div>
    <h2>Appuyer sur un bouton pour commencer :</h2>
  </div>
</template>

<style scoped>
#start-container {
  display: flex;
  flex-direction: column;
  justify-content: center; /* alignement vertical */
  align-items: center;     /* alignement horizontal */
  text-align: center;
  height: 100vh;           /* toute la hauteur de la page */
}

#logo {
  width: 300px;
  height: 300px;
  background-image: url('/images/logo.jpg'); 
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  margin-bottom: 20px;
}

h2 {
  color: #000;
  font-size: 48px;
}
</style>
