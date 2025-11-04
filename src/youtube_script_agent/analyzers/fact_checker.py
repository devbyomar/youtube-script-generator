"""
Fact-checking for viral claims
"""

import json
from langchain_core.messages import HumanMessage
from typing import Dict, List
from ..core.state import AgentState


def fact_check_claims(state: AgentState, llm) -> AgentState:
    """
    Fact-check viral claims before including them
    
    Args:
        state: Current agent state with filtered_tweets
        llm: Claude LLM instance
        
    Returns:
        Updated state with fact_check_results
    """
    print("✅ Fact-checking viral claims...")
    
    if state.get('error') or not state['filtered_tweets']:
        return state
    
    # Extract claims that need verification
    top_tweets = state['filtered_tweets'][:10]
    
    claims_to_check = []
    for tweet in top_tweets:
        # Identify tweets with strong claims or stats
        if any(indicator in tweet['text'].lower() for indicator in 
               ['breaking:', 'report:', 'sources:', 'confirmed:', '%', 'first time', 'record']):
            claims_to_check.append({
                'tweet_id': tweet['id'],
                'text': tweet['text'],
                'author': tweet['author_username'],
                'engagement': tweet['total_engagement']
            })
    
    fact_check_results = []
    
    if claims_to_check:
        prompt = f"""You are a fact-checker. Analyze these viral claims and rate their credibility:

{json.dumps(claims_to_check[:5], indent=2)}

For each claim:
1. Identify the specific factual claim being made
2. Rate credibility: HIGH (likely true), MEDIUM (needs context), LOW (likely false/misleading)
3. Provide brief reasoning
4. Suggest how to present it safely (e.g., "add qualifier", "verify first", "safe to use")

Return JSON array with: tweet_id, claim, credibility, reasoning, recommendation"""
        
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            content = response.content
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            
            fact_check_results = json.loads(content.strip())
            
            # Add fact-check results to tweets
            fact_check_map = {fc['tweet_id']: fc for fc in fact_check_results}
            for tweet in state['filtered_tweets']:
                if tweet['id'] in fact_check_map:
                    tweet['fact_check'] = fact_check_map[tweet['id']]
            
            print(f"✅ Fact-checked {len(fact_check_results)} claims")
            
        except Exception as e:
            print(f"⚠️ Fact-check error: {e}")
    
    state['fact_check_results'] = fact_check_results
    return state