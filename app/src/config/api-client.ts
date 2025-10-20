import { createClient } from '../lib/client/client.gen';

export const apiClient = createClient({
  baseUrl: process.env.API_BASE_URL || 'http://localhost:8080',
});
