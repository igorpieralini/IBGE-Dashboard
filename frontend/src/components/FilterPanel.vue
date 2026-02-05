<template>
  <div class="filter-panel">
    <div class="filter-group" v-if="showPeriod">
      <label>Período</label>
      <select v-model="filters.period" @change="emit">
        <option value="12">Últimos 12 meses</option>
        <option value="24">Últimos 2 anos</option>
        <option value="36">Últimos 3 anos</option>
        <option value="60">Últimos 5 anos</option>
      </select>
    </div>
    
    <div class="filter-group" v-if="showRegion">
      <label>Região</label>
      <select v-model="filters.region" @change="emit">
        <option value="">Brasil</option>
        <option value="1">Norte</option>
        <option value="2">Nordeste</option>
        <option value="3">Sudeste</option>
        <option value="4">Sul</option>
        <option value="5">Centro-Oeste</option>
      </select>
    </div>
    
    <div class="filter-group" v-if="showIndicator">
      <label>Indicador</label>
      <select v-model="filters.indicator" @change="emit">
        <option value="unemployment">Taxa de Desocupação</option>
        <option value="occupied">Pessoas Ocupadas</option>
        <option value="income">Rendimento Médio</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  showPeriod: { type: Boolean, default: true },
  showRegion: { type: Boolean, default: false },
  showIndicator: { type: Boolean, default: false },
  initialPeriod: { type: String, default: '24' },
  initialRegion: { type: String, default: '' },
  initialIndicator: { type: String, default: 'unemployment' }
})

const emits = defineEmits(['change'])

const filters = reactive({
  period: props.initialPeriod,
  region: props.initialRegion,
  indicator: props.initialIndicator
})

const emit = () => emits('change', { ...filters })
</script>

<style scoped>
.filter-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.filter-group label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-group select {
  padding: 0.6rem 2rem 0.6rem 0.8rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  font-size: 0.95rem;
  color: #0f172a;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
}

.filter-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}
</style>
