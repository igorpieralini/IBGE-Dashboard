<template>
  <div class="analise">
    <header class="page-header">
      <h1>Análises Detalhadas</h1>
      <p>Compare indicadores por diferentes segmentos da população</p>
    </header>

    <nav class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="{ active: activeTab === tab.id }"
        @click="selectTab(tab.id)"
      >
        {{ tab.label }}
      </button>
    </nav>

    <LoadingSpinner v-if="loading" message="Carregando análise..." />
    
    <ErrorMessage v-else-if="error" :message="error" @retry="loadData" />

    <template v-else>
      <section class="tab-content">
        <ChartCard 
          :title="currentTitle"
          :series="chartData"
          type="line"
          :unit="currentUnit"
        />
      </section>

      <section class="data-table" v-if="tableData.length">
        <h3>Dados Recentes</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Categoria</th>
                <th>Valor Atual</th>
                <th>Período</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableData" :key="row.name">
                <td>{{ row.name }}</td>
                <td class="value">{{ formatValue(row.value) }}</td>
                <td class="period">{{ row.period }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="insights" v-if="insights.length">
        <h3>Insights</h3>
        <div class="insights-grid">
          <div class="insight-card" v-for="(insight, i) in insights" :key="i">
            <p>{{ insight }}</p>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  getAnalysisBySex, 
  getAnalysisByRace, 
  getAnalysisByAge, 
  getAnalysisByEducation, 
  getAnalysisByRegion 
} from '../services/ibgeApi'
import ChartCard from '../components/ChartCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorMessage from '../components/ErrorMessage.vue'

const tabs = [
  { id: 'sex', label: 'Sexo' },
  { id: 'race', label: 'Raça/Cor' },
  { id: 'age', label: 'Faixa Etária' },
  { id: 'education', label: 'Escolaridade' },
  { id: 'region', label: 'Região' }
]

const titles = {
  sex: 'Taxa de Desocupação por Sexo',
  race: 'Taxa de Desocupação por Raça/Cor',
  age: 'Taxa de Desocupação por Faixa Etária',
  education: 'Taxa de Desocupação por Escolaridade',
  region: 'Taxa de Desocupação por Região'
}

const activeTab = ref('sex')
const loading = ref(true)
const error = ref(null)
const analysisData = ref({})

const latestPoint = (series) =>
  (Array.isArray(series) && series.length ? series[series.length - 1] : null)

const currentTitle = computed(() => titles[activeTab.value])
const currentUnit = computed(() => '%')

const chartData = computed(() => {
  const d = analysisData.value[activeTab.value]
  if (!d?.categories) return []
  return d.categories
})

const tableData = computed(() => {
  const d = analysisData.value[activeTab.value]
  if (!d?.categories) return []
  
  return d.categories.map(cat => {
    const latest = latestPoint(cat.series)
    return {
      name: cat.name,
      value: latest?.value,
      period: latest?.period
    }
  })
})

const insights = computed(() => {
  const d = analysisData.value[activeTab.value]
  if (!d?.categories || d.categories.length < 2) return []
  
  const result = []
  const sorted = [...d.categories]
    .map(c => ({ name: c.name, value: latestPoint(c.series)?.value }))
    .filter(c => c.value !== null)
    .sort((a, b) => b.value - a.value)
  
  if (sorted.length >= 2) {
    const highest = sorted[0]
    const lowest = sorted[sorted.length - 1]
    const diff = highest.value - lowest.value
    
    result.push(`${highest.name}: maior taxa de desocupação (${highest.value.toFixed(1)}%)`)
    result.push(`${lowest.name}: menor taxa de desocupação (${lowest.value.toFixed(1)}%)`)
    result.push(`Diferença entre extremos: ${diff.toFixed(1)} pontos percentuais`)
  }
  
  return result
})

const formatValue = (val) => {
  if (val === null || val === undefined) return '-'
  return `${val.toFixed(1)}%`
}

const selectTab = (tabId) => {
  if (activeTab.value === tabId) return
  activeTab.value = tabId
  loadData()
}

const loadData = async () => {
  loading.value = true
  error.value = null
  
  const fetchers = {
    sex: getAnalysisBySex,
    race: getAnalysisByRace,
    age: getAnalysisByAge,
    education: getAnalysisByEducation,
    region: getAnalysisByRegion
  }
  
  try {
    const result = await fetchers[activeTab.value]()
    analysisData.value = { ...analysisData.value, [activeTab.value]: result }
  } catch (e) {
    error.value = 'Não foi possível carregar os dados desta análise.'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.analise {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.5rem;
}

.page-header p {
  color: #64748b;
  margin: 0;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #f1f5f9;
  border-radius: 12px;
  margin-bottom: 2rem;
  overflow-x: auto;
}

.tabs button {
  flex: 1;
  padding: 0.8rem 1.5rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.tabs button:hover {
  color: #0f172a;
}

.tabs button.active {
  background: white;
  color: #3b82f6;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.tab-content {
  margin-bottom: 2rem;
}

.data-table {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 2rem;
}

.data-table h3 {
  font-size: 1.1rem;
  color: #0f172a;
  margin: 0 0 1rem;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

th {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

td {
  color: #0f172a;
}

td.value {
  font-weight: 600;
  color: #3b82f6;
}

td.period {
  color: #94a3b8;
  font-size: 0.9rem;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background: #f8fafc;
}

.insights {
  margin-top: 2rem;
}

.insights h3 {
  font-size: 1.2rem;
  color: #0f172a;
  margin: 0 0 1rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.insight-card {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-radius: 12px;
  padding: 1.25rem;
  border-left: 4px solid #3b82f6;
}

.insight-card p {
  margin: 0;
  color: #1e40af;
  font-size: 0.95rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .analise {
    padding: 1rem;
  }
  
  .tabs {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .tabs button {
    flex: none;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
  }
  
  .insights-grid {
    grid-template-columns: 1fr;
  }
}
</style>
