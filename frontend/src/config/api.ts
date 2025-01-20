// URL de base de l'API
export const API_BASE_URL = 'https://authwebapp124.azurewebsites.net';

// export const API_BASE_URL = 'http://localhost:8000';

// Fonction utilitaire pour construire l'URL complète
export const getApiUrl = (path: string) => `${API_BASE_URL}${path}`;
