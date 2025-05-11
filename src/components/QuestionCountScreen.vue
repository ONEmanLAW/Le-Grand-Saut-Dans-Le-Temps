<template>
  <div class="screen">
    <h1>Choisissez le nombre de questions</h1>
    <div class="choices">
      <button v-for="(count, index) in [4, 8]" :key="count" @click="select(count)">
        <span class="label">{{ letters[index] }}</span> {{ count }}
      </button>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['selected'])
function select(count) {
  emit('selected', count)
}

const letters = ['A', 'B', 'C', 'D'] // on peut aller jusqu’à D
</script>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #ffc800;
  text-align: center;
}

h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 52px;
  margin-bottom: 40px;
}

.choices {
  display: flex;
  gap: 50px;
}

button {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px;
  font-size: 2rem;
  padding: 30px 60px;
  width: 280px;
  height: 150px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: 0.2s;
  justify-content: center;
}

button:hover {
  background-color: #555;
}

.label {
  font-weight: bold;
  font-size: 2rem;
  background-color: white;
  color: #333;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
