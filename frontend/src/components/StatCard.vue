<template>
  <div class="stat-card" :class="colorClass">
    <div class="stat-icon">
      <slot name="icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
          <polyline points="16 7 22 7 22 13"/>
        </svg>
      </slot>
    </div>
    <div class="stat-info">
      <span class="stat-label">{{ label }}</span>
      <span class="stat-value">{{ formattedValue }}</span>
      <span v-if="trend !== null && trend !== undefined" class="stat-trend" :class="trendClass">
        {{ trend > 0 ? '▲' : '▼' }} {{ formatTrend }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  value: [Number, String],
  unit: { type: String, default: '' },
  trend: { type: Number, default: null },
  color: { type: String, default: 'blue' },
  invertTrend: { type: Boolean, default: false }
})

const formattedValue = computed(() => {
  if (props.value === null || props.value === undefined || props.value === '-') return '—'
  const num = Number(props.value)
  if (isNaN(num)) return props.value
  if (props.unit === '%') return `${num.toFixed(1)}%`
  if (props.unit === 'R$') return `R$ ${num.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
  if (props.unit === 'mil' || props.unit === 'milhões') return `${num.toLocaleString('pt-BR')} ${props.unit}`
  return `${props.value} ${props.unit}`.trim()
})

const colorClass = computed(() => `card-${props.color}`)

const formatTrend = computed(() => {
  if (props.trend === null || props.trend === undefined) return ''
  return Math.abs(props.trend).toFixed(1)
})

const trendClass = computed(() => {
  if (props.trend === null) return ''
  const isPositive = props.invertTrend ? props.trend < 0 : props.trend > 0
  return isPositive ? 'trend-up' : 'trend-down'
})
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.card-blue .stat-icon { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); }
.card-green .stat-icon { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.card-orange .stat-icon { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.card-purple .stat-icon { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); }
.card-red .stat-icon { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
}

.stat-trend {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  width: fit-content;
}

.trend-up { background: #dcfce7; color: #16a34a; }
.trend-down { background: #fee2e2; color: #dc2626; }
</style>
