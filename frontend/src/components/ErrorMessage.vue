<template>
  <div class="error-box">
    <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 8v4M12 16h.01"/>
    </svg>
    <div class="error-content">
      <h4>{{ title || 'Erro ao carregar dados' }}</h4>
      <p>{{ message }}</p>
    </div>
    <button v-if="retry" @click="$emit('retry')" class="retry-btn">
      Tentar novamente
    </button>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  message: String,
  retry: { type: Boolean, default: true }
})

defineEmits(['retry'])
</script>

<style scoped>
.error-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  gap: 1rem;
}

.error-icon {
  width: 48px;
  height: 48px;
  color: #ef4444;
}

.error-content h4 {
  margin: 0;
  color: #991b1b;
  font-weight: 600;
}

.error-content p {
  margin: 0.5rem 0 0;
  color: #b91c1c;
  font-size: 0.9rem;
}

.retry-btn {
  padding: 0.6rem 1.5rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #dc2626;
}
</style>
