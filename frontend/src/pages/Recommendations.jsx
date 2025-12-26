import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import RecommendationCard from '../components/RecommendationCard';
import api from '../services/api';

export default function Recommendations() {
  const [searchParams] = useSearchParams();
  const [flights, setFlights] = useState([]);
  const [selectedFlight, setSelectedFlight] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [assignModal, setAssignModal] = useState(null);
  const [assigning, setAssigning] = useState(false);
  const [assignSuccess, setAssignSuccess] = useState(null);

  useEffect(() => {
    loadFlights();
  }, []);

  useEffect(() => {
    const flightParam = searchParams.get('flight');
    if (flightParam) {
      setSelectedFlight(flightParam);
      loadRecommendations(flightParam);
    }
  }, [searchParams]);

  const loadFlights = async () => {
    try {
      const response = await api.getAllFlights();
      setFlights(response.data);
    } catch (error) {
      console.error('Error loading flights:', error);
    }
  };

  const loadRecommendations = async (flightNumber) => {
    if (!flightNumber) return;
    setLoading(true);
    try {
      const response = await api.getRecommendations(flightNumber);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error loading recommendations:', error);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFlightChange = (e) => {
    const flight = e.target.value;
    setSelectedFlight(flight);
    loadRecommendations(flight);
  };

  const handleAssign = (rec) => {
    setAssignModal(rec);
  };

  const confirmAssign = async () => {
    if (!assignModal) return;
    
    setAssigning(true);
    
    try {
      // Call backend API to assign crew
      const response = await api.assignCrewToFlight(assignModal.emp_id, selectedFlight);
      
      console.log('Assignment successful:', response.data);
      
      // Show success message
      setAssignSuccess({
        crewName: assignModal.name,
        flightNumber: selectedFlight
      });
      
      // Close modal
      setAssignModal(null);
      
      // Reload recommendations to remove assigned crew from available pool
      setTimeout(() => {
        loadRecommendations(selectedFlight);
        setAssignSuccess(null);
      }, 3000);
      
    } catch (error) {
      console.error('Assignment failed:', error);
      
      // Show error message
      const errorMsg = error.response?.data?.error || 'Failed to assign crew';
      alert(`Error: ${errorMsg}`);
      
    } finally {
      setAssigning(false);
    }
  };

  const selectedFlightData = flights.find(f => f.flightNumber === selectedFlight);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          ⭐ 17-Parameter Crew Recommendations
        </h2>
        <div className="flex items-center gap-4">
          <label className="font-semibold text-gray-700">Select Flight:</label>
          <select
            value={selectedFlight}
            onChange={handleFlightChange}
            className="flex-1 max-w-md px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          >
            <option value="">Choose a flight...</option>
            {flights.map((flight) => (
              <option key={flight.flightNumber} value={flight.flightNumber}>
                {flight.flightNumber} {flight.route} ({flight.crewRequired - flight.crewAssigned}/{flight.crewRequired})
              </option>
            ))}
          </select>
        </div>
      </div>

      {selectedFlight && selectedFlightData && (
        <div className="mb-6">
          <h3 className="text-xl font-bold text-gray-900">
            Top 5 Recommendations for {selectedFlightData.flightNumber} ({selectedFlightData.route})
          </h3>
        </div>
      )}

      {loading && (
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
        </div>
      )}

      {!loading && recommendations.length === 0 && selectedFlight && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <p className="text-yellow-800 text-lg">⚠️ No recommendations available for this flight.</p>
          <p className="text-yellow-600 text-sm mt-2">All qualified crew may already be assigned.</p>
        </div>
      )}

      {!loading && recommendations.length > 0 && (
        <div className="space-y-6">
          {recommendations.map((rec) => (
            <RecommendationCard
              key={rec.emp_id}
              recommendation={rec}
              rank={rec.rank}
              onAssign={handleAssign}
            />
          ))}
        </div>
      )}

      {/* Success Notification */}
      {assignSuccess && (
        <div className="fixed top-4 right-4 z-50 bg-green-500 text-white px-6 py-4 rounded-lg shadow-2xl flex items-center gap-3 animate-slide-in">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <div>
            <p className="font-bold">Assignment Successful!</p>
            <p className="text-sm">{assignSuccess.crewName} assigned to {assignSuccess.flightNumber}</p>
          </div>
        </div>
      )}

      {/* Assignment Confirmation Modal */}
      {assignModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full">
            <h3 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              ✓ Confirm Assignment
            </h3>
            <div className="bg-blue-50 rounded-lg p-4 mb-4">
              <div className="flex items-center gap-3 mb-2">
                <div className="text-4xl">✈️</div>
                <div>
                  <p className="font-bold text-lg">{selectedFlightData.flightNumber}</p>
                  <p className="text-gray-600">{selectedFlightData.aircraft}</p>
                </div>
              </div>
              <div className="text-sm text-gray-600">
                <p>Route: <span className="font-semibold">{selectedFlightData.route}</span></p>
                <p>Departure: <span className="font-semibold">{selectedFlightData.departure}</span></p>
              </div>
            </div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center text-xl font-bold">
                {assignModal.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0,2)}
              </div>
              <div>
                <p className="font-bold text-lg">{assignModal.name}</p>
                <p className="text-gray-600">{assignModal.designation} • {assignModal.baseLocation}</p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-2 mb-6 text-center">
              <div className="bg-gray-50 p-2 rounded">
                <p className="text-sm text-gray-600">Experience</p>
                <p className="font-bold">15 yrs</p>
              </div>
              <div className="bg-gray-50 p-2 rounded">
                <p className="text-sm text-gray-600">Rating</p>
                <p className="font-bold">{(assignModal.compositeScore / 20).toFixed(1)}/5</p>
              </div>
              <div className="bg-gray-50 p-2 rounded">
                <p className="text-sm text-gray-600">Hours</p>
                <p className="font-bold">4,100</p>
              </div>
            </div>
            <p className="text-gray-700 mb-6">Are you sure you want to assign this crew member to this flight?</p>
            <div className="flex gap-3">
              <button
                onClick={() => setAssignModal(null)}
                disabled={assigning}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmAssign}
                disabled={assigning}
                className={`flex-1 px-4 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center justify-center gap-2 ${
                  assigning ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {assigning ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Assigning...
                  </>
                ) : (
                  <>
                    ✓ Confirm Assignment
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
