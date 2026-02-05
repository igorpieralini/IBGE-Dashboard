import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

const get = async (url, config) => {
  const response = await api.get(url, config)
  return response.data
}

export const getUnemployment = () => get('/ibge/unemployment')
export const getUnemploymentSummary = () => get('/ibge/unemployment/summary')
export const getOccupied = () => get('/ibge/occupied')
export const getIncome = () => get('/ibge/income')
export const getInformality = () => get('/ibge/informality')

export const getAnalysisBySex = (indicator = 'unemployment') =>
  get('/analysis/sex', { params: { indicator } })
export const getAnalysisByRace = (indicator = 'unemployment') =>
  get('/analysis/race', { params: { indicator } })
export const getAnalysisByAge = () => get('/analysis/age')
export const getAnalysisByEducation = (indicator = 'unemployment') =>
  get('/analysis/education', { params: { indicator } })
export const getAnalysisByRegion = (indicator = 'unemployment') =>
  get('/analysis/region', { params: { indicator } })
