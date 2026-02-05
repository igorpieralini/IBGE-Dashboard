<template>
  <div class="loading-overlay" :class="{ fullscreen }">
    <div class="spinner"></div>
    <p v-if="message" class="loading-text">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  message: String,
  fullscreen: { type: Boolean, default: false }
})
</script>

<style scoped>
.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  gap: 1rem;
}

.loading-overlay.fullscreen {
  position: fixed;
  inset: 0;
  background: rgba(255,255,255,0.9);
  z-index: 1000;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-text {
  color: #64748b;
  font-size: 0.95rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
