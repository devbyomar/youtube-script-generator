"""
Competitor content analysis
"""

import json
from langchain_core.messages import HumanMessage
from typing import Dict, List
from ..core.state import AgentState
import tweepy


def analyze_competitors(state: AgentState, twitter_client: tweepy.Client, llm) -> AgentState:
    """
    Analyze what competitor channels are covering
    
    Args:
        state: Current agent state
        twitter_client: Authenticated Twitter client
        llm: Claude LLM instance
        
    Returns:
        Updated state with competitor_analysis
    """
    print("🎯 Analyzing competitor content...")
    
    if state.get('error'):
        return state
    
    config = state['config']
    competitor_channels = config.get('competitor_channels', [])
    
    try:
        competitor_topics = []
        
        # Search tweets from competitor channels
        for channel in competitor_channels:
            query = f"from:{channel.replace('@', '')} -is:retweet"
            tweets = twitter_client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['public_metrics', 'created_at']
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    competitor_topics.append({
                        'channel': channel,
                        'text': tweet.text,
                        'engagement': tweet.public_metrics['like_count'] + tweet.public_metrics['retweet_count']
                    })
        
        # Use Claude to analyze competitor patterns
        if competitor_topics:
            prompt = f"""Analyze what these competitor channels are covering:

{json.dumps(competitor_topics[:20], indent=2)}

Identify:
1. Common themes they're all covering (we should too)
2. Gaps they're missing (opportunities for us)
3. Their content angles (to differentiate ourselves)

Return JSON with: common_themes (list), gaps (list), competitor_angles (list)"""
            
            response = llm.invoke([HumanMessage(content=prompt)])
            content = response.content
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            
            state['competitor_analysis'] = json.loads(content.strip())
            print("✅ Competitor analysis complete")
        else:
            state['competitor_analysis'] = {'common_themes': [], 'gaps': [], 'competitor_angles': []}
            
    except Exception as e:
        print(f"⚠️ Competitor analysis error: {e}")
        state['competitor_analysis'] = {'error': str(e)}
    
    return state