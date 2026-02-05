<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>Dados do Mercado de Trabalho Brasileiro</h1>
        <p>Visualize e analise indicadores econômicos do IBGE com gráficos interativos e dados atualizados</p>
        <div class="hero-actions">
          <router-link to="/dashboard" class="btn-primary">Ver Dashboard</router-link>
          <router-link to="/analise" class="btn-secondary">Análises Detalhadas</router-link>
        </div>
      </div>
      <div class="hero-visual">
        <div class="data-preview">
          <div class="preview-header">
            <span class="dot red"></span>
            <span class="dot yellow"></span>
            <span class="dot green"></span>
          </div>
          <div class="preview-content">
            <div class="preview-line"></div>
            <div class="preview-line short"></div>
            <div class="preview-chart">
              <svg viewBox="0 0 200 60">
                <path d="M0,50 Q30,45 50,35 T100,30 T150,20 T200,25" 
                      stroke="#3b82f6" fill="none" stroke-width="2"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="stats-section" v-if="!loading && stats">
      <div class="stats-grid">
        <StatCard 
          label="Taxa de Desocupação"
          :value="stats.unemployment?.latest"
          unit="%"
          :trend="stats.unemployment?.trend"
          color="blue"
        />
        <StatCard 
          label="Pessoas Ocupadas"
          :value="formatMillion(stats.occupied?.latest)"
          unit="milhões"
          :trend="stats.occupied?.trend"
          color="green"
        />
        <StatCard 
          label="Rendimento Médio"
          :value="formatCurrency(stats.income?.latest)"
          unit=""
          :trend="stats.income?.trend"
          color="purple"
        />
      </div>
      <p class="stats-note">Dados mais recentes disponíveis da PNAD Contínua - IBGE</p>
    </section>

    <LoadingSpinner v-else-if="loading" message="Carregando indicadores..." />

    <section class="features">
      <h2>O que você encontra aqui</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </div>
          <h3>Dashboard Interativo</h3>
          <p>Gráficos de evolução temporal dos principais indicadores do mercado de trabalho</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="M21 21l-4.35-4.35"/>
            </svg>
          </div>
          <h3>Análises por Segmento</h3>
          <p>Compare dados por sexo, raça/cor, faixa etária, escolaridade e região</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
              <polyline points="16 7 22 7 22 13"/>
            </svg>
          </div>
          <h3>Dados Atualizados</h3>
          <p>Informações diretamente da API do IBGE, sempre com os dados mais recentes</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s-8-4.5-8-11.8A8 8 0 0112 2a8 8 0 018 8.2c0 7.3-8 11.8-8 11.8z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
          </div>
          <h3>Cobertura Nacional</h3>
          <p>Dados para o Brasil e todas as grandes regiões geográficas</p>
        </div>
      </div>
    </section>

    <section class="about">
      <h2>Sobre os Dados</h2>
      <p>
        Os indicadores apresentados são provenientes da <strong>Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua)</strong>, 
        conduzida pelo IBGE. Esta pesquisa produz indicadores trimestrais sobre a força de trabalho e outras informações 
        necessárias para o estudo do desenvolvimento socioeconômico do País.
      </p>
      <div class="source-badge">
        <span>Fonte:</span>
        <a href="https://www.ibge.gov.br/estatisticas/sociais/trabalho.html" target="_blank">
          IBGE - Instituto Brasileiro de Geografia e Estatística
        </a>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUnemployment, getOccupied, getIncome } from '../services/ibgeApi'
import StatCard from '../components/StatCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'

const loading = ref(true)
const stats = ref(null)

const formatMillion = (val) => {
  if (!val) return '-'
  return (val / 1000).toFixed(1)
}

const formatCurrency = (val) => {
  if (!val) return '-'
  return `R$ ${val.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}`
}

onMounted(async () => {
  try {
    const [unemp, occ, inc] = await Promise.all([
      getUnemployment(),
      getOccupied(),
      getIncome()
    ])
    stats.value = {
      unemployment: unemp.summary,
      occupied: occ.summary,
      income: inc.summary
    }
  } catch (e) {
    stats.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  padding: 3rem 0 4rem;
}

.hero-content h1 {
  font-size: 2.8rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.2;
  margin: 0 0 1rem;
}

.hero-content p {
  font-size: 1.2rem;
  color: #64748b;
  margin: 0 0 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn-primary, .btn-secondary {
  padding: 0.9rem 2rem;
  border-radius: 10px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59,130,246,0.4);
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.hero-visual {
  display: flex;
  justify-content: center;
}

.data-preview {
  width: 100%;
  max-width: 400px;
  background: #0f172a;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(15,23,42,0.3);
}

.preview-header {
  padding: 0.8rem 1rem;
  background: #1e293b;
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
.dot.red { background: #ef4444; }
.dot.yellow { background: #eab308; }
.dot.green { background: #22c55e; }

.preview-content {
  padding: 1.5rem;
}

.preview-line {
  height: 12px;
  background: #334155;
  border-radius: 6px;
  margin-bottom: 0.8rem;
}
.preview-line.short {
  width: 60%;
}

.preview-chart {
  margin-top: 1.5rem;
  background: #1e293b;
  border-radius: 8px;
  padding: 1rem;
}

.preview-chart svg {
  width: 100%;
  height: 60px;
}

.stats-section {
  margin: 2rem 0 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.stats-note {
  text-align: center;
  color: #94a3b8;
  font-size: 0.85rem;
  margin-top: 1rem;
}

.features {
  padding: 3rem 0;
}

.features h2 {
  text-align: center;
  font-size: 1.8rem;
  color: #0f172a;
  margin: 0 0 2rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.feature-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.feature-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 1rem;
  padding: 12px;
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-radius: 12px;
  color: #3b82f6;
}

.feature-icon svg {
  width: 100%;
  height: 100%;
}

.feature-card h3 {
  font-size: 1.1rem;
  color: #0f172a;
  margin: 0 0 0.5rem;
}

.feature-card p {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.about {
  background: #f8fafc;
  border-radius: 16px;
  padding: 2.5rem;
  margin: 2rem 0;
}

.about h2 {
  font-size: 1.5rem;
  color: #0f172a;
  margin: 0 0 1rem;
}

.about p {
  color: #475569;
  line-height: 1.7;
  margin: 0 0 1.5rem;
}

.source-badge {
  display: inline-flex;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
}

.source-badge span {
  color: #64748b;
}

.source-badge a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.source-badge a:hover {
  text-decoration: underline;
}

@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .hero-visual {
    display: none;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
