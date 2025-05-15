<template>
  <div class="waiting-scan-container">
    <p>En attente du scan du badge…</p>
  </div>
</template>

<script>
export default {
  name: 'WaitingScan',
}
</script>

<style scoped>
.waiting-scan-container {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 52px;
  font-weight: bold;
  color: black;
}
</style>
