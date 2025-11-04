"""
Quality filtering and tweet scoring
"""

from typing import Dict, List
from ..core.state import AgentState


def filter_quality_tweets_advanced(state: AgentState) -> AgentState:
    """
    Advanced filtering with configurable thresholds and bot detection
    
    Args:
        state: Current agent state with raw_tweets
        
    Returns:
        Updated state with filtered_tweets
    """
    print("🔎 Applying advanced quality filters...")
    
    if state.get('error'):
        return state
    
    config = state['config']
    filtered = []
    
    for tweet in state['raw_tweets']:
        # Configurable thresholds
        meets_engagement = tweet['total_engagement'] >= config['engagement_threshold']
        good_ratio = tweet['engagement_ratio'] >= 0.001
        has_meaningful_likes = tweet['likes'] >= (config['engagement_threshold'] * 0.4)
        
        # Detect bot-like behavior
        reasonable_rt_ratio = tweet['retweets'] <= tweet['likes'] * 2
        not_spam = tweet['replies'] <= tweet['total_engagement'] * 0.8
        
        # Source credibility with configurable follower threshold
        reputable_source = (
            tweet['author_verified'] or 
            tweet['author_followers'] >= config['follower_threshold'] or
            tweet['total_engagement'] >= config['engagement_threshold'] * 4
        )
        
        # Quality score calculation
        quality_score = (
            (tweet['likes'] * 1.0) +
            (tweet['retweets'] * 2.0) +
            (tweet['replies'] * 1.5) +
            (tweet['quotes'] * 3.0) +
            (100 if tweet['author_verified'] else 0)
        )
        tweet['quality_score'] = quality_score
        
        if (meets_engagement and good_ratio and has_meaningful_likes and 
            reasonable_rt_ratio and not_spam and reputable_source):
            filtered.append(tweet)
    
    # Sort by quality score
    state['filtered_tweets'] = sorted(filtered, key=lambda x: x['quality_score'], reverse=True)[:50]
    print(f"✅ Filtered to {len(state['filtered_tweets'])} high-quality tweets")
    
    return state