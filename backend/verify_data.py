import json

# Load and verify crew data
with open('data/crew_data.json', 'r', encoding='utf-8') as f:
    crew_data = json.load(f)

print("="*70)
print(f"CREW DATA VERIFICATION")
print("="*70)
print(f"\nTotal crew members: {len(crew_data)}")

# Check data structure
required_fields = [
    'emp_id', 'name', 'designation', 'baseLocation', 'availability',
    'certifications', 'yearsExperience', 'totalFlightHours',
    'fatigueScore', 'restPeriodScore', 'consecutiveDutyScore',
    'medicalStatusScore', 'performanceScore', 'onTimeRecordScore',
    'skillProficiencyScore', 'reliabilityScore', 'backoutHistoryScore',
    'seniorityScore', 'flightHoursScore', 'locationScore',
    'availabilityScore', 'dutyComplianceScore', 'certificationValidityScore',
    'languageProficiencyScore', 'routeFamiliarityScore'
]

# Verify first entry
print("\n--- Sample Entry (First Crew Member) ---")
first_crew = crew_data[0]
print(f"ID: {first_crew.get('emp_id')}")
print(f"Name: {first_crew.get('name')}")
print(f"Designation: {first_crew.get('designation')}")
print(f"Base: {first_crew.get('baseLocation')}")

# Check for missing fields
missing_fields = []
for field in required_fields:
    if field not in first_crew:
        missing_fields.append(field)

if missing_fields:
    print(f"\n⚠ WARNING: Missing fields: {missing_fields}")
else:
    print(f"\n✓ All {len(required_fields)} required fields present")

# Statistics
designations = {}
locations = {}
certifications_count = {}
availability_status = {}

for crew in crew_data:
    # Designation distribution
    desg = crew.get('designation', 'Unknown')
    designations[desg] = designations.get(desg, 0) + 1
    
    # Location distribution
    loc = crew.get('baseLocation', 'Unknown')
    locations[loc] = locations.get(loc, 0) + 1
    
    # Availability status
    avail = crew.get('availability', 'Unknown')
    availability_status[avail] = availability_status.get(avail, 0) + 1
    
    # Certifications
    for cert in crew.get('certifications', []):
        certifications_count[cert] = certifications_count.get(cert, 0) + 1

print("\n" + "="*70)
print("DATA DISTRIBUTION ANALYSIS")
print("="*70)

print("\nCrew by Designation:")
for desg, count in sorted(designations.items()):
    print(f"   {desg}: {count} ({count/len(crew_data)*100:.1f}%)")

print("\nCrew by Base Location:")
for loc, count in sorted(locations.items()):
    print(f"   {loc}: {count} ({count/len(crew_data)*100:.1f}%)")

print("\nCrew by Aircraft Certification:")
for cert, count in sorted(certifications_count.items()):
    print(f"   {cert}: {count} crew members certified")

print("\nAvailability Status:")
for status, count in sorted(availability_status.items()):
    print(f"   {status}: {count} ({count/len(crew_data)*100:.1f}%)")

# Score analysis
avg_fatigue = sum(c.get('fatigueScore', 0) for c in crew_data) / len(crew_data)
avg_performance = sum(c.get('performanceScore', 0) for c in crew_data) / len(crew_data)
avg_reliability = sum(c.get('reliabilityScore', 0) for c in crew_data) / len(crew_data)

print("\nAverage Scores:")
print(f"   Fatigue Score: {avg_fatigue:.2f}")
print(f"   Performance Score: {avg_performance:.2f}")
print(f"   Reliability Score: {avg_reliability:.2f}")

# Find top 5 performers
crew_scores = [(c['name'], c.get('performanceScore', 0)) for c in crew_data]
crew_scores.sort(key=lambda x: x[1], reverse=True)

print("\nTop 5 Performers:")
for i, (name, score) in enumerate(crew_scores[:5], 1):
    print(f"   {i}. {name}: {score}")

print("\n" + "="*70)
print("✓ DATA VERIFICATION COMPLETE")
print("="*70)
