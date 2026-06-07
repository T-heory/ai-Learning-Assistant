import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export function createSessionId(): string {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8)
}

export const api = {
  health: () => request.get('/health'),
  chat: (message: string, sessionId: string = 'default') =>
    request.post('/chat', { message, session_id: sessionId }),
  chatStream: (message: string, sessionId: string = 'default') =>
    request.post('/chat/stream', { message, session_id: sessionId }, { responseType: 'stream', adapter: 'fetch' }),
  callAgent: (agentName: string, inputData: Record<string, any>) =>
    request.post(`/agents/${agentName}`, { agent_type: agentName, input_data: inputData }),
  generateResources: (topic: string, sessionId: string = 'default') =>
    request.post('/resources/generate', { topic, session_id: sessionId }),
  planPath: (topic: string, sessionId: string = 'default') =>
    request.post('/path/plan', { topic, session_id: sessionId }),
  adjustPath: (data: Record<string, any>) =>
    request.post('/path/adjust', data),
  evaluate: (sessionId: string = 'default', answers: any[] = []) =>
    request.post('/evaluate', { session_id: sessionId, answers }),
  getProfile: (sessionId: string = 'default') =>
    request.get(`/profile/${sessionId}`),
}

export default api
