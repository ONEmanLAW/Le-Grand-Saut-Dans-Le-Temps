<template>
  <div class="screen">
    <h1>Choisissez le nombre de questions</h1>
    <div class="choices">
      <button v-for="(count, index) in [4, 8, 16, 20]" :key="count" @click="select(count)" :class="colorClasses[index]">
        {{ count }} 
      </button>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['selected'])
function select(count) {
  emit('selected', count)
}

const colorClasses = ['red', 'blue', 'yellow', 'green']
</script>

<style scoped>
 .screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 52px;
  margin-bottom: 40px;
  color: black;
  padding: 50px;
}

.choices {
  display: flex;
  gap: 50px;
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  font-size: 2rem;
  padding: 30px 50px;
  width: 175px;
  height: 175px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: 0.2s;
  position: relative;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.red {
  background-color: red;
}

.blue {
  background-color: blue;
}

.yellow {
  background-color: #C89214;
}

.green {
  background-color: green;
}

</style>
