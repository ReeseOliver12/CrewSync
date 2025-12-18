import heapq
from collections import defaultdict

# ============================================
# DATA STRUCTURE IMPLEMENTATIONS
# ============================================

class CrewMember:
    """Node representation for crew member"""
    def __init__(self, data):
        self.emp_id = data['emp_id']
        self.name = data['name']
        self.designation = data['designation']
        
        # Handle both 'baseLocation' (camelCase) and 'baselocation' (lowercase)
        self.base_location = data.get('baseLocation') or data.get('baselocation', 'UNKNOWN')
        
        self.data = data
    
    def __repr__(self):
        return f"Crew({self.emp_id}, {self.name})"


class MinHeapCrewScheduler:
    """
    Min-Heap for fatigue-based crew selection
    Complexity: O(log n) for insert/extract
    Use Case: Get least fatigued crew member quickly
    """
    def __init__(self):
        self.heap = []
    
    def insert(self, crew, fatigue_score):
        heapq.heappush(self.heap, (100 - fatigue_score, crew))
        print(f"   [HEAP INSERT] {crew.name} with fatigue score {fatigue_score}")
    
    def get_least_fatigued(self):
        if self.heap:
            fatigue, crew = heapq.heappop(self.heap)
            actual_fatigue = 100 - fatigue
            print(f"   [HEAP EXTRACT-MIN] {crew.name} (fatigue: {actual_fatigue})")
            return crew
        return None
    
    def size(self):
        return len(self.heap)


class CertificationHashMap:
    """
    Hash Map for O(1) crew filtering by certification
    Complexity: O(1) for lookup
    Use Case: Instantly find crew certified for specific aircraft
    """
    def __init__(self):
        self.cert_map = defaultdict(list)
    
    def add_crew(self, crew):
        for cert in crew.data.get('certifications', []):
            self.cert_map[cert].append(crew)
        certs_str = ', '.join(crew.data.get('certifications', []))
        print(f"   [HASH MAP INSERT] {crew.name} → [{certs_str}]")
    
    def get_by_certification(self, cert_type):
        result = self.cert_map.get(cert_type, [])
        print(f"   [HASH MAP LOOKUP] '{cert_type}' → Found {len(result)} crew members")
        return result


class LocationGraph:
    """
    Graph for connection feasibility
    Complexity: O(1) for edge check, O(V + E) for DFS traversal
    Use Case: Check if crew can reach flight origin
    """
    def __init__(self):
        self.adjacency = defaultdict(set)
    
    def add_route(self, origin, destination):
        self.adjacency[origin].add(destination)
        print(f"   [GRAPH ADD EDGE] {origin} → {destination}")
    
    def can_reach(self, crew_location, flight_origin):
        # Direct connection check (O(1))
        result = flight_origin in self.adjacency.get(crew_location, set()) or crew_location == flight_origin
        status = "✓ YES" if result else "✗ NO"
        print(f"   [GRAPH CHECK] Can {crew_location} reach {flight_origin}? {status}")
        return result
    
    def find_affected_flights(self, disrupted_location):
        """
        DFS traversal to find all affected flights
        Complexity: O(V + E)
        """
        print(f"   [GRAPH DFS] Finding flights affected by disruption at {disrupted_location}")
        affected = []
        visited = set()
        
        def dfs(location):
            if location in visited:
                return
            visited.add(location)
            affected.append(location)
            for neighbor in self.adjacency.get(location, []):
                dfs(neighbor)
        
        dfs(disrupted_location)
        print(f"   [GRAPH DFS RESULT] {len(affected)} locations affected: {affected}")
        return affected


class BSTRankingTree:
    """
    Binary Search Tree for performance-based ranking
    Complexity: O(k + log n) for top-K extraction
    Use Case: Get top performers efficiently
    """
    class Node:
        def __init__(self, crew, score):
            self.crew = crew
            self.score = score
            self.left = None
            self.right = None
    
    def __init__(self):
        self.root = None
        self.size_count = 0
    
    def insert(self, crew, score):
        print(f"   [BST INSERT] {crew.name} with composite score {score:.2f}")
        self.root = self._insert_recursive(self.root, crew, score)
        self.size_count += 1
    
    def _insert_recursive(self, node, crew, score):
        if not node:
            return self.Node(crew, score)
        if score >= node.score:
            node.right = self._insert_recursive(node.right, crew, score)
        else:
            node.left = self._insert_recursive(node.left, crew, score)
        return node
    
    def get_top_k(self, k):
        """
        Reverse in-order traversal to get top K performers
        Complexity: O(k + log n)
        """
        result = []
        self._inorder_reverse(self.root, result, k)
        print(f"   [BST RANGE QUERY] Retrieved top {len(result)} performers from {self.size_count} total")
        return result
    
    def _inorder_reverse(self, node, result, k):
        if not node or len(result) >= k:
            return
        self._inorder_reverse(node.right, result, k)
        if len(result) < k:
            result.append((node.crew, node.score))
        self._inorder_reverse(node.left, result, k)


class BackupCrewQueue:
    """
    Queue for standby crew management (FIFO)
    Complexity: O(1) for enqueue/dequeue
    Use Case: Manage backup crew in order of availability
    """
    def __init__(self):
        self.queue = []
    
    def enqueue(self, crew):
        self.queue.append(crew)
        print(f"   [QUEUE ENQUEUE] {crew.name} added to backup (position: {len(self.queue)})")
    
    def dequeue(self):
        if self.queue:
            crew = self.queue.pop(0)
            print(f"   [QUEUE DEQUEUE] {crew.name} removed from backup ({len(self.queue)} remaining)")
            return crew
        print(f"   [QUEUE DEQUEUE] Queue is empty!")
        return None
    
    def peek(self):
        if self.queue:
            return self.queue[0]
        return None
    
    def size(self):
        return len(self.queue)