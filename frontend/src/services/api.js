import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export const api = {
  // Dashboard
  getDashboardStats: () => axios.get(`${API_BASE}/dashboard/stats`),
  
  // Flights
  getAllFlights: () => axios.get(`${API_BASE}/flights`),
  getFlightById: (flightNumber) => axios.get(`${API_BASE}/flights/${flightNumber}`),
  
  // Crew
  getAllCrew: () => axios.get(`${API_BASE}/crew`),
  getCrewById: (empId) => axios.get(`${API_BASE}/crew/${empId}`),
  
  // Recommendations
  getRecommendations: (flightNumber) => axios.get(`${API_BASE}/recommendations/${flightNumber}`),
  
  // Assignment - NEW
  assignCrewToFlight: (empId, flightNumber) => 
    axios.post(`${API_BASE}/crew/${empId}/assign`, { 
      flight_number: flightNumber 
    }),
  
  // Health
  healthCheck: () => axios.get(`${API_BASE}/health`),
};

export default api;
