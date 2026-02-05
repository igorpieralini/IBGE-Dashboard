<template>
  <header class="header">
    <div class="header-content">
      <router-link to="/" class="logo">
        <img src="/logo.svg" alt="Logo" class="logo-img" />
        <span class="logo-text">IBGE Dashboard</span>
      </router-link>
      <nav class="nav">
        <router-link to="/" class="nav-link">Início</router-link>
        <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/analise" class="nav-link">Análise</router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.logo-img {
  width: 40px;
  height: 40px;
}

.logo-text {
  font-size: 1.4rem;
  font-weight: 700;
  color: #fff;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #fff;
  background: rgba(255,255,255,0.1);
}

@media (max-width: 768px) {
  .header { padding: 0 1rem; }
  .logo-text { display: none; }
  .nav { gap: 0.5rem; }
  .nav-link { padding: 0.5rem; font-size: 0.9rem; }
}
</style>
