import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plane, Users, AlertTriangle, TrendingUp } from 'lucide-react';
import StatsCard from '../components/StatsCard';
import FlightCard from '../components/FlightCard';
import api from '../services/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('default'); // ✅ NEW

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, flightsRes] = await Promise.all([
        api.getDashboardStats(),
        api.getAllFlights(),
      ]);
      setStats(statsRes.data);
      setFlights(flightsRes.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
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

  // ✅ SORT LOGIC
  const getSortedFlights = () => {
    const flightsCopy = [...flights];
    
    if (sortBy === 'priority-high') {
      return flightsCopy.sort((a, b) => {
        const priorityOrder = { 'High': 1, 'Medium': 2, 'Low': 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });
    }
    
    if (sortBy === 'priority-low') {
      return flightsCopy.sort((a, b) => {
        const priorityOrder = { 'Low': 1, 'Medium': 2, 'High': 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });
    }
    
    return flightsCopy;
  };

  const sortedFlights = getSortedFlights();

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Flights"
          value={stats?.totalFlights || 0}
          subtitle="Today's schedule"
          icon={<Plane className="w-8 h-8" />}
          color="blue"
        />
        <StatsCard
          title="Available Crew"
          value={stats?.availableCrew || 0}
          subtitle="of 8 total"
          icon={<Users className="w-8 h-8" />}
          color="green"
        />
        <StatsCard
          title="Needs Assignment"
          value={stats?.needsAssignment || 0}
          subtitle="Requires attention"
          icon={<AlertTriangle className="w-8 h-8" />}
          color="red"
        />
        <StatsCard
          title="Avg Performance"
          value={stats?.avgPerformance || 0}
          subtitle="Passenger rating"
          icon={<TrendingUp className="w-8 h-8" />}
          color="purple"
        />
      </div>

      {/* Flight Schedule */}
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <div className="px-6 py-4 bg-gray-50 border-b">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
              ✈️ Flight Schedule
            </h2>
            
            {/* ✅ SORTING DROPDOWN */}
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium text-gray-700">Sort by:</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm font-medium"
              >
                <option value="default">Default Order</option>
                <option value="priority-high">High Priority First</option>
                <option value="priority-low">Low Priority First</option>
              </select>
            </div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Flight</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Route</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aircraft</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Departure</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priority</th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Crew</th>
              </tr>
            </thead>
            <tbody>
              {sortedFlights.map((flight) => (
                <FlightCard
                  key={flight.flightNumber}
                  flight={flight}
                  onClick={() => navigate(`/recommendations?flight=${flight.flightNumber}`)}
                />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
