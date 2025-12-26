import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import CrewTable from '../components/CrewTable';
import api from '../services/api';

export default function CrewManagement() {
  const [crew, setCrew] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    loadCrew();
  }, [location]); // Refetch when navigating to this page

  const loadCrew = async () => {
    setLoading(true);
    try {
      const response = await api.getAllCrew();
      setCrew(response.data);
    } catch (error) {
      console.error('Error loading crew:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          👥 Crew Members ({crew.length})
        </h2>
      </div>
      <CrewTable crew={crew} />
    </div>
  );
}
