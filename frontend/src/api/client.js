import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const api = {
    predict: async (data) => {
        const response = await client.post('/predict', data);
        return response.data;
    },
    getMetrics: async () => {
        const response = await client.get('/metrics');
        return response.data;
    },
    getAlerts: async (limit = 10) => {
        const response = await client.get(`/alerts?limit=${limit}`);
        return response.data;
    },
};
