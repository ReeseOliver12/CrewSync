from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from recommendation_engine import CrewRecommendationEngine

app = Flask(__name__)
CORS(app)

# Load data
def load_json_data(filename):
    """Load JSON data from data directory"""
    filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(filepath, 'r') as f:
        return json.load(f)

CREW_DATA = load_json_data('crew_data.json')
FLIGHT_DATA = load_json_data('flights_data.json')

# Initialize recommendation engine
recommendation_engine = CrewRecommendationEngine(CREW_DATA)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'crew_count': len(CREW_DATA),
        'flight_count': len(FLIGHT_DATA)
    })

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Count available crew (case-insensitive)
        available_crew = sum(
            1 for crew in CREW_DATA 
            if crew.get('availability', '').lower() == 'available'
        )
        
        # Count flights needing crew
        needs_assignment = sum(
            1 for flight in FLIGHT_DATA 
            if flight.get('crewAssigned', 0) < flight.get('crewRequired', 6)
        )
        
        # Calculate average performance
        total_performance = sum(crew.get('performanceScore', 0) for crew in CREW_DATA)
        avg_performance = round((total_performance / len(CREW_DATA)) / 20, 1) if CREW_DATA else 0
        
        return jsonify({
            'totalFlights': len(FLIGHT_DATA),
            'availableCrew': available_crew,
            'needsAssignment': needs_assignment,
            'avgPerformance': avg_performance
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/flights', methods=['GET'])
def get_all_flights():
    """Get all flights"""
    return jsonify(FLIGHT_DATA)

@app.route('/api/flights/<flight_number>', methods=['GET'])
def get_flight_by_number(flight_number):
    """Get specific flight details"""
    flight = next((f for f in FLIGHT_DATA if f['flightNumber'] == flight_number), None)
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    return jsonify(flight)

@app.route('/api/crew', methods=['GET'])
def get_all_crew():
    """Get all crew members"""
    return jsonify(CREW_DATA)

@app.route('/api/crew/<emp_id>', methods=['GET'])
def get_crew_by_id(emp_id):
    """Get specific crew member details"""
    crew = next((c for c in CREW_DATA if str(c['emp_id']) == str(emp_id)), None)
    if not crew:
        return jsonify({'error': 'Crew member not found'}), 404
    return jsonify(crew)

@app.route('/api/recommendations/<flight_number>', methods=['GET'])
def get_recommendations(flight_number):
    """Get crew recommendations for a specific flight"""
    try:
        # Find flight
        flight = next((f for f in FLIGHT_DATA if f['flightNumber'] == flight_number), None)
        if not flight:
            return jsonify({'error': f'Flight {flight_number} not found'}), 404
        
        # Get recommendations from engine
        recommendations = recommendation_engine.get_recommendations(flight, top_k=5)
        
        return jsonify(recommendations)
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ✅ NEW ENDPOINT - ASSIGN CREW TO FLIGHT
@app.route('/api/crew/<emp_id>/assign', methods=['POST'])
def assign_crew_to_flight(emp_id):
    """Assign crew member to a flight and update their availability status"""
    try:
        # Get flight number from request body
        data = request.get_json()
        flight_number = data.get('flight_number')
        
        if not flight_number:
            return jsonify({'error': 'flight_number is required'}), 400
        
        # Load current crew data
        crew_file_path = os.path.join(os.path.dirname(__file__), 'data', 'crew_data.json')
        with open(crew_file_path, 'r') as f:
            crew_data = json.load(f)
        
        # Find the crew member by emp_id (handle both string and int IDs)
        crew_member = None
        crew_index = None
        for idx, crew in enumerate(crew_data):
            if str(crew.get('emp_id')) == str(emp_id):
                crew_member = crew
                crew_index = idx
                break
        
        if not crew_member:
            return jsonify({'error': f'Crew member {emp_id} not found'}), 404
        
        # Check if already assigned
        if crew_member.get('availability', '').lower() != 'available':
            return jsonify({
                'error': f'{crew_member["name"]} is not available (current status: {crew_member.get("availability")})'
            }), 400
        
        # Update crew member status
        crew_data[crew_index]['availability'] = 'Assigned'
        crew_data[crew_index]['assignedFlight'] = flight_number
        
        # Save updated data back to JSON file
        with open(crew_file_path, 'w') as f:
            json.dump(crew_data, f, indent=2)
        
        # Update global CREW_DATA variable
        global CREW_DATA
        CREW_DATA = crew_data
        
        print(f"\n✓ ASSIGNMENT SUCCESSFUL: {crew_member['name']} (ID: {emp_id}) → Flight {flight_number}")
        print(f"  Status changed: Available → Assigned\n")
        
        return jsonify({
            'success': True,
            'message': f'{crew_member["name"]} assigned to flight {flight_number}',
            'crew': {
                'emp_id': crew_member['emp_id'],
                'name': crew_member['name'],
                'availability': 'Assigned',
                'assignedFlight': flight_number
            }
        }), 200
        
    except Exception as e:
        print(f"Error assigning crew: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("CREWSYNC BACKEND SERVER")
    print("="*70)
    print(f"Loaded {len(CREW_DATA)} crew members")
    print(f"Loaded {len(FLIGHT_DATA)} flights")
    print("\nServer starting on http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
