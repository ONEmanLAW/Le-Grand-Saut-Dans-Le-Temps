<template>
  <div id="start-container">
    <div id="logo" @click="$emit('start')"></div>
    <h2>Bienvenue ! Cliquez pour commencer.</h2>
  </div>
</template>


<style scoped>
#start-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #FFC800;
  text-align: center;
}

#logo {
  width: 200px;
  height: 200px;
  background-image: url('/images/logo.jpg'); 
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  margin-bottom: 20px;
}

h2 {
  color: #000; 
}
</style>
