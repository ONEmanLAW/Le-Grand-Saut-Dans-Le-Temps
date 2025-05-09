<template>
  <div class="screen">
    <h1>Choisissez le nombre de questions</h1>
    <div class="choices">
      <button v-for="count in [4, 8]" :key="count" @click="select(count)">
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
</script>

  
  <style scoped>
  .choices {
    display: flex;
    gap: 20px;
    margin-top: 40px;
  }
  button {
    font-size: 1.5rem;
    padding: 10px 20px;
    background-color: #333;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.2s;
  }
  button:hover {
    background-color: #555;
  }
  </style>
  