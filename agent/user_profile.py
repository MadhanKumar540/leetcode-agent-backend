# In-memory store for session states
# Structure: { "session_id": { "level": "beginner", "score": 0 } }
user_profiles = {}

def analyze_query(query: str) -> int:
    """
    Analyzes the query and returns a complexity score adjustment.
    Beginner keywords: -1
    Intermediate keywords: +1
    Advanced keywords: +2
    """
    query_lower = query.lower()
    score = 0
    
    # Beginner keywords
    if any(k in query_lower for k in ["what is", "explain", "i don't understand", "lost", "stuck", "confused", "help"]):
        score -= 1
        
    # Intermediate keywords
    if any(k in query_lower for k in ["approach", "optimize", "time complexity", "space complexity", "better way"]):
        score += 1
        
    # Advanced keywords
    if any(k in query_lower for k in ["optimal", "o(n)", "o(1)", "space optimization", "edge case", "monotonic", "dp", "memoization"]):
        score += 2
        
    return score

def update_and_get_level(session_id: str, initial_level: str, query: str) -> str:
    """
    Updates the session score based on the query and resolves the current level.
    """
    initial_level = initial_level.lower()
    
    # Initialize session if missing
    if session_id not in user_profiles:
        # Give a starting score based on manual selection
        starting_score = -1
        if initial_level == "intermediate":
            starting_score = 3
        elif initial_level == "advanced":
            starting_score = 6
            
        user_profiles[session_id] = {
            "level": initial_level,
            "score": starting_score
        }
        
    # Analyze query and update score
    score_delta = analyze_query(query)
    current_score = user_profiles[session_id]["score"] + score_delta
    
    # Bound the score loosely to prevent extreme runaway (-5 to 10)
    current_score = max(-5, min(current_score, 10))
    user_profiles[session_id]["score"] = current_score
    
    # Evaluate new level
    new_level = "beginner"
    if current_score >= 6:
        new_level = "advanced"
    elif current_score >= 1:
        new_level = "intermediate"
        
    user_profiles[session_id]["level"] = new_level
    return new_level
