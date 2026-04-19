from agent.prompt import build_prompt
from llm.model import generate_response

def detect_intent(query: str) -> str:
    query_lower = query.lower()
    if "pattern" in query_lower:
        return "PATTERN"
    elif "hint" in query_lower:
        return "HINT"
    elif "approach" in query_lower or "explain" in query_lower or "how to solve" in query_lower or "algorithm" in query_lower:
        return "APPROACH"
    elif "code" in query_lower or "solution" in query_lower:
        return "CODE"
    else:
        return "GENERAL"

def process_query(problem_title: str, problem_description: str, user_query: str, history: list) -> dict:
    intent = detect_intent(user_query)
    
    prompt = build_prompt(
        problem_title=problem_title,
        problem_description=problem_description,
        query=user_query,
        intent=intent
    )
    
    # Optional: pass history to the LLM context
    generated_text = generate_response(prompt, history)
    
    return {
        "type": intent.lower(),
        "content": generated_text
    }
