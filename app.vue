<template>
  <div class="app-container">
    <ClientOnly>
      <StarfieldBackground />
    </ClientOnly>
    <Navigation />
    <main class="main-content">
      <NuxtPage />
    </main>
    <ClientOnly>
      <ParticleCursor />
    </ClientOnly>
  </div>
</template>

<script setup>
</script>

<style lang="scss">
.app-container {
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;
}

.main-content {
  position: relative;
  z-index: 10;
}
</style>
