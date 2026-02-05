<template>
  <div class="chart-card">
    <h3 class="chart-title">{{ title }}</h3>
    <div class="chart-container">
      <canvas ref="chartRef"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  title: String,
  series: Array,
  type: { type: String, default: 'line' },
  unit: { type: String, default: '%' }
})

const chartRef = ref(null)
let chart = null

const colors = [
  'rgb(59, 130, 246)', 'rgb(239, 68, 68)', 'rgb(34, 197, 94)',
  'rgb(168, 85, 247)', 'rgb(249, 115, 22)', 'rgb(236, 72, 153)'
]

const renderChart = async () => {
  await nextTick()
  if (!chartRef.value) return
  if (!props.series || props.series.length === 0) return
  if (chart) {
    chart.destroy()
    chart = null
  }

  const isMulti = props.series[0]?.series !== undefined
  
  let labels, datasets
  
  if (isMulti) {
    const allPeriods = [...new Set(props.series.flatMap(s => s.series.map(p => p.period)))].sort().slice(-24)
    labels = allPeriods
    datasets = props.series.map((s, i) => ({
      label: s.name,
      data: allPeriods.map(p => s.series.find(pt => pt.period === p)?.value || null),
      borderColor: colors[i % colors.length],
      backgroundColor: colors[i % colors.length].replace('rgb', 'rgba').replace(')', ', 0.1)'),
      tension: 0.3,
      fill: props.type === 'line'
    }))
  } else {
    const data = props.series.slice(-24)
    labels = data.map(d => d.period)
    datasets = [{
      label: 'Valor',
      data: data.map(d => d.value),
      borderColor: colors[0],
      backgroundColor: props.type === 'bar' 
        ? colors[0].replace('rgb', 'rgba').replace(')', ', 0.7)')
        : colors[0].replace('rgb', 'rgba').replace(')', ', 0.1)'),
      tension: 0.3,
      fill: props.type === 'line'
    }]
  }

  chart = new Chart(chartRef.value, {
    type: props.type,
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: isMulti, position: 'top' },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const val = ctx.raw
              if (val === null) return `${ctx.dataset.label}: -`
              if (props.unit === 'R$') return `${ctx.dataset.label}: R$ ${val.toLocaleString('pt-BR')}`
              return `${ctx.dataset.label}: ${val.toFixed(1)}${props.unit}`
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: props.unit === '%',
          ticks: {
            callback: (v) => props.unit === 'R$' ? `R$ ${(v/1000).toFixed(0)}k` : `${v}${props.unit}`
          }
        }
      }
    }
  })
}

onMounted(() => renderChart())
watch(() => props.series, () => renderChart(), { deep: true, immediate: true })
</script>

<style scoped>
.chart-card {
  background: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.chart-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 1rem 0;
}

.chart-container {
  height: 300px;
}
</style>
