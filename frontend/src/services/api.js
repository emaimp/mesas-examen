import axios from 'axios';

// Crea una instancia de Axios
export const api = axios.create({
  // Asegúrate de que esta URL sea la de tu backend
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

