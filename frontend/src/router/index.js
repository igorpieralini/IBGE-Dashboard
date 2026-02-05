import { createRouter, createWebHistory } from 'vue-router'

const HomePage = () => import('../pages/HomePage.vue')
const DashboardPage = () => import('../pages/DashboardPage.vue')
const AnalisePage = () => import('../pages/AnalisePage.vue')

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/dashboard', name: 'Dashboard', component: DashboardPage },
  { path: '/analise', name: 'Analise', component: AnalisePage }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
