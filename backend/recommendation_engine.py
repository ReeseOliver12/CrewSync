from data_structures import *
import re
import random


class CrewRecommendationEngine:
    """
    17-Parameter Algorithmic Recommendation System
    NO ML/AI - Pure data structure-driven decision making
    """
    
    # Parameter weights (total = 100%)
    WEIGHTS = {
        'fatigueScore': 0.15,
        'restPeriodScore': 0.10,
        'consecutiveDutyScore': 0.08,
        'medicalStatusScore': 0.07,
        'performanceScore': 0.10,
        'onTimeRecordScore': 0.08,
        'skillProficiencyScore': 0.07,
        'reliabilityScore': 0.08,
        'backoutHistoryScore': 0.07,
        'seniorityScore': 0.05,
        'flightHoursScore': 0.05,
        'locationScore': 0.03,
        'availabilityScore': 0.02,
        'dutyComplianceScore': 0.02,
        'certificationValidityScore': 0.01,
        'languageProficiencyScore': 0.01,
        'routeFamiliarityScore': 0.01
    }
    
    def __init__(self, crew_data):
        self.crew_members = [CrewMember(c) for c in crew_data]
        
        # Initialize all data structures
        self.cert_hashmap = CertificationHashMap()
        self.location_graph = LocationGraph()
        self.fatigue_heap = MinHeapCrewScheduler()
        self.backup_queue = BackupCrewQueue()
        
        self._initialize_data_structures()
    
    def _initialize_data_structures(self):
        """Populate all data structures with crew data"""
        print("\n" + "="*70)
        print("INITIALIZING DATA STRUCTURES")
        print("="*70)
        
        print("\n[1] HASH MAP - Certification Index")
        for crew in self.crew_members:
            self.cert_hashmap.add_crew(crew)
        
        print("\n[2] MIN-HEAP - Fatigue Monitoring")
        for crew in self.crew_members:
            self.fatigue_heap.insert(crew, crew.data.get('fatigueScore', 50))
        
        print("\n[3] QUEUE - Backup Crew Management")
        for crew in self.crew_members:
            if crew.data.get('availability') == 'Backup':
                self.backup_queue.enqueue(crew)
        
        print("\n[4] GRAPH - Location Network")
        locations = ['DEL', 'BOM', 'BLR', 'HYD', 'GOI']
        for loc1 in locations:
            for loc2 in locations:
                if loc1 != loc2:
                    self.location_graph.add_route(loc1, loc2)
        
        print("\n" + "="*70)
        print(f"✓ Initialized {len(self.crew_members)} crew members across all data structures")
        print("="*70 + "\n")
    
    def calculate_composite_score(self, crew_data, flight_data=None):
        """Calculate weighted composite score from all 17 parameters"""
        score = 0
        for param, weight in self.WEIGHTS.items():
            param_score = crew_data.get(param, 0)
            score += param_score * weight
        
        return round(score, 2)
    
    def _format_parameter_name(self, param_name):
        """Convert camelCase parameter name to readable format"""
        name = param_name.replace('Score', '')
        name = re.sub(r'([A-Z])', r' \1', name)
        return name.strip()
    
    def get_recommendations(self, flight_data, top_k=5):
        """
        Main recommendation algorithm - FLIGHT SPECIFIC VERSION
        Forces different crew for different flights based on base location priority
        """
        print("\n" + "="*70)
        print(f"RECOMMENDATION ENGINE: {flight_data['flightNumber']} ({flight_data['route']})")
        print("="*70)
        
        # STEP 1: Filter by certification using Hash Map (O(1))
        print(f"\n[STEP 1] HASH MAP FILTERING - Aircraft: {flight_data['aircraft']}")
        print("-" * 70)
        eligible_crew = self.cert_hashmap.get_by_certification(flight_data['aircraft'])
        print(f"   Result: {len(eligible_crew)} crew members certified for {flight_data['aircraft']}")
        
        # STEP 2: Filter by availability (case-insensitive)
        print(f"\n[STEP 2] AVAILABILITY FILTERING")
        print("-" * 70)
        available_crew = [
            c for c in eligible_crew 
            if c.data.get('availability', '').lower() == 'available'
        ]
        print(f"   Available crew: {len(available_crew)} out of {len(eligible_crew)}")
        
        if len(available_crew) > 0:
            for crew in available_crew[:5]:
                print(f"   ✓ {crew.name} - {crew.base_location}")
            if len(available_crew) > 5:
                print(f"   ... and {len(available_crew) - 5} more")
        
        if len(available_crew) == 0:
            print(f"\n   ⚠ WARNING: No available crew found!")
            return []
        
        # STEP 3: Check location feasibility using Graph (O(1) per check)
        print(f"\n[STEP 3] GRAPH CONNECTIVITY CHECK")
        print("-" * 70)
        origin = flight_data['origin']
        reachable_crew = []
        for crew in available_crew:
            can_reach = self.location_graph.can_reach(crew.base_location, origin)
            if can_reach:
                reachable_crew.append(crew)
        print(f"   Result: {len(reachable_crew)} crew can reach {origin}")
        
        if len(reachable_crew) == 0:
            print(f"\n   ⚠ WARNING: No crew can reach {origin}!")
            return []
        
        # STEP 4: AGGRESSIVE FILTERING - Prioritize by base location
        print(f"\n[STEP 4] LOCATION-BASED PRIORITY FILTERING")
        print("-" * 70)
        
        # Separate crew by location priority
        at_origin = []
        near_origin = []
        others = []
        
        for crew in reachable_crew:
            base = crew.base_location
            if base == origin:
                at_origin.append(crew)
            elif base == flight_data.get('destination'):
                near_origin.append(crew)
            else:
                others.append(crew)
        
        print(f"   Crew at origin ({origin}): {len(at_origin)}")
        print(f"   Crew at destination ({flight_data.get('destination')}): {len(near_origin)}")
        print(f"   Other locations: {len(others)}")
        
        # STEP 5: Score and rank with HEAVY location weighting
        print(f"\n[STEP 5] WEIGHTED SCORING WITH LOCATION BOOST")
        print("-" * 70)
        
        crew_scores = []
        
        # Process crew at origin (HUGE bonus)
        for crew in at_origin:
            base_score = self.calculate_composite_score(crew.data, flight_data)
            boosted_score = base_score + 20 + random.uniform(0, 5)  # +20-25 bonus
            crew_scores.append((crew, boosted_score))
            print(f"   {crew.name} (AT {origin}): {base_score:.2f} → {boosted_score:.2f} (+20 location bonus)")
        
        # Process crew near destination (medium bonus)
        for crew in near_origin:
            base_score = self.calculate_composite_score(crew.data, flight_data)
            boosted_score = base_score + 10 + random.uniform(0, 3)  # +10-13 bonus
            crew_scores.append((crew, boosted_score))
            print(f"   {crew.name} (NEAR DEST): {base_score:.2f} → {boosted_score:.2f} (+10 bonus)")
        
        # Process other crew (small bonus to create variety)
        for crew in others:
            base_score = self.calculate_composite_score(crew.data, flight_data)
            # Add random factor based on flight number to vary results
            flight_num = int(''.join(filter(str.isdigit, flight_data.get('flightNumber', '0'))))
            seed_factor = (flight_num % 10) + random.uniform(0, 5)
            boosted_score = base_score + seed_factor
            crew_scores.append((crew, boosted_score))
        
        # Sort by score (highest first)
        crew_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Take top K
        top_recommendations = crew_scores[:top_k]
        
        # Format recommendations
        print(f"\n[STEP 6] TOP {top_k} RECOMMENDATIONS FOR {flight_data['flightNumber']}")
        print("-" * 70)
        
        recommendations = []
        for idx, (crew, score) in enumerate(top_recommendations, 1):
            key_strengths = [
                self._format_parameter_name(k)
                for k, v in crew.data.items() 
                if k.endswith('Score') and v > 85
            ]
            
            rec = {
                'rank': idx,
                'emp_id': crew.emp_id,
                'name': crew.name,
                'designation': crew.designation,
                'baseLocation': crew.base_location,
                'compositeScore': round(score, 2),
                'parameters': {k: crew.data.get(k, 0) for k in self.WEIGHTS.keys()},
                'weights': self.WEIGHTS,
                'keyStrengths': key_strengths
            }
            recommendations.append(rec)
            print(f"   #{idx} {crew.name} ({crew.base_location}) - Score: {score:.2f}")
        
        print("\n" + "="*70)
        print(f"✓ RECOMMENDATION COMPLETE - {len(recommendations)} UNIQUE candidates for {flight_data['flightNumber']}")
        print("="*70 + "\n")
        
        return recommendations
    
    def demonstrate_heap_operation(self):
        """Demonstrate min-heap fatigue extraction"""
        print("\n" + "="*70)
        print("DEMONSTRATING MIN-HEAP - Get Least Fatigued Crew")
        print("="*70)
        print(f"\nHeap size: {self.fatigue_heap.size()}")
        print("Extracting top 3 least fatigued crew members:\n")
        
        for i in range(min(3, self.fatigue_heap.size())):
            crew = self.fatigue_heap.get_least_fatigued()
            if crew:
                print(f"   Position {i+1}: {crew.name}")
        
        print("\n" + "="*70 + "\n")
