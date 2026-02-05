<template>
  <div class="dashboard">
    <header class="page-header">
      <h1>Dashboard</h1>
      <p>Acompanhe a evolução dos principais indicadores do mercado de trabalho</p>
    </header>

    <LoadingSpinner v-if="loading" message="Carregando dados do IBGE..." />
    
    <ErrorMessage v-else-if="error" :message="error" @retry="loadData" />

    <template v-else>
      <section class="summary-cards">
        <StatCard 
          label="Taxa de Desocupação"
          :value="dashboardData.unemployment?.summary?.latest"
          unit="%"
          :trend="dashboardData.unemployment?.summary?.trend"
          color="blue"
        />
        <StatCard 
          label="Variação Anual"
          :value="dashboardData.unemployment?.summary?.trend"
          unit="p.p."
          :trend="dashboardData.unemployment?.summary?.trend"
          color="green"
        />
        <StatCard 
          label="Pessoas Ocupadas"
          :value="formatMillions(dashboardData.occupied?.summary?.latest)"
          unit="milhões"
          :trend="dashboardData.occupied?.summary?.trend"
          color="purple"
        />
        <StatCard 
          label="Rendimento Médio"
          :value="formatCurrency(dashboardData.income?.summary?.latest)"
          unit=""
          :trend="dashboardData.income?.summary?.trend"
          color="orange"
        />
      </section>

      <section class="charts-grid">
        <ChartCard 
          title="Taxa de Desocupação (%)"
          :series="dashboardData.unemployment?.series"
          type="line"
          unit="%"
        />
        <ChartCard 
          title="Pessoas Ocupadas (mil)"
          :series="dashboardData.occupied?.series"
          type="line"
          unit=" mil"
        />
        <ChartCard 
          title="Rendimento Médio Real (R$)"
          :series="dashboardData.income?.series"
          type="bar"
          unit="R$"
        />
        <ChartCard 
          title="Massa de Rendimento (Milhões R$)"
          :series="dashboardData.mass?.series"
          type="line"
          unit="R$"
        />
      </section>

      <section class="info-section">
        <div class="info-card">
          <h3>Período dos Dados</h3>
          <p>{{ dashboardData.unemployment?.summary?.latestPeriod || 'Não disponível' }}</p>
        </div>
        <div class="info-card">
          <h3>Fonte</h3>
          <p>PNAD Contínua - IBGE</p>
        </div>
        <div class="info-card">
          <h3>Atualização</h3>
          <p>Trimestral móvel</p>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUnemployment, getOccupied, getIncome, getInformality } from '../services/ibgeApi'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorMessage from '../components/ErrorMessage.vue'

const loading = ref(true)
const error = ref(null)
const dashboardData = ref({})

const formatMillions = (val) => (val ? (val / 1000).toFixed(1) : '-')
const formatCurrency = (val) =>
  (val ? `R$ ${val.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}` : '-')

const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const [unemployment, occupied, income, mass] = await Promise.all([
      getUnemployment(),
      getOccupied(),
      getIncome(),
      getInformality()
    ])
    
    dashboardData.value = { unemployment, occupied, income, mass }
  } catch (e) {
    error.value = 'Não foi possível carregar os dados. Verifique sua conexão e tente novamente.'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.dashboard {
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

.summary-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.info-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.info-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
}

.info-card h3 {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0 0 0.5rem;
  font-weight: 500;
}

.info-card p {
  font-size: 1rem;
  color: #0f172a;
  margin: 0;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .dashboard {
    padding: 1rem;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .info-section {
    grid-template-columns: 1fr;
  }
}
</style>
