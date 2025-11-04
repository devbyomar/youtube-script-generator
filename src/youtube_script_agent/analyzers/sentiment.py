"""
Advanced sentiment analysis with competitor context
"""

import json
from langchain_core.messages import HumanMessage
from typing import Dict
from ..core.state import AgentState


def analyze_sentiment_advanced(state: AgentState, llm) -> AgentState:
    """
    Advanced sentiment analysis with competitor context
    
    Args:
        state: Current agent state with filtered_tweets
        llm: Claude LLM instance
        
    Returns:
        Updated state with sentiment_analysis
    """
    print("🧠 Running advanced sentiment analysis...")
    
    if state.get('error') or not state['filtered_tweets']:
        return state
    
    tweets_summary = []
    for tweet in state['filtered_tweets'][:20]:
        tweets_summary.append({
            'text': tweet['text'],
            'engagement': tweet['total_engagement'],
            'quality_score': tweet['quality_score'],
            'author': tweet['author_username'],
            'verified': tweet['author_verified'],
            'top_comments': [c['text'] for c in tweet.get('comments', [])[:5]],
            'fact_check': tweet.get('fact_check', {})
        })
    
    competitor_context = state.get('competitor_analysis', {})
    
    prompt = f"""Analyze these top tweets and provide comprehensive insights:

TWEETS:
{json.dumps(tweets_summary, indent=2)}

COMPETITOR COVERAGE:
{json.dumps(competitor_context, indent=2)}

TRENDING HASHTAGS:
{', '.join(state['trending_hashtags'][:10])}

Provide:
1. **Overall Sentiment**: Dominant mood and why
2. **Trending Topics**: Ranked by importance (top 10)
3. **Controversies**: Debates generating discussion
4. **Viral Moments**: Most shared moments/plays
5. **Comment Patterns**: What people are saying in replies
6. **Unique Angles**: What competitors aren't covering
7. **Content Opportunities**: Specific video ideas
8. **Viewer Emotions**: What emotions to tap into

Format as JSON with keys: sentiment, trending_topics (list), controversies (list), viral_moments (list), comment_insights (list), unique_angles (list), content_opportunities (list), viewer_emotions (list)"""
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        
        analysis = json.loads(content.strip())
        state['sentiment_analysis'] = analysis
        state['trending_topics'] = analysis.get('trending_topics', [])
        print("✅ Advanced sentiment analysis complete")
        
    except Exception as e:
        print(f"⚠️ Analysis error: {e}")
        state['sentiment_analysis'] = {'error': str(e)}
    
    return state