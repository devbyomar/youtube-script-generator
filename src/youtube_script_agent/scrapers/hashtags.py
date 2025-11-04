"""
Hashtag discovery and trending topic identification
"""

import tweepy
from datetime import datetime, timedelta
from typing import Dict, List
from ..core.state import AgentState


def discover_trending_hashtags(state: AgentState, twitter_client: tweepy.Client) -> AgentState:
    """
    Dynamically discover trending hashtags for the topic
    
    Args:
        state: Current agent state
        twitter_client: Authenticated Twitter client
        
    Returns:
        Updated state with trending_hashtags
    """
    print(f"🔥 Discovering trending hashtags for {state['topic']}...")
    
    try:
        config = state['config']
        now = datetime.utcnow()
        start_time = now - timedelta(hours=24)
        
        # Search for trending content
        base_query = config['search_base']
        tweets = twitter_client.search_recent_tweets(
            query=f"{base_query} -is:retweet lang:en",
            start_time=start_time.isoformat() + "Z",
            max_results=100,
            tweet_fields=['entities', 'public_metrics']
        )
        
        # Extract and count hashtags
        hashtag_counts = {}
        if tweets.data:
            for tweet in tweets.data:
                if tweet.entities and 'hashtags' in tweet.entities:
                    for tag in tweet.entities['hashtags']:
                        hashtag = tag['tag'].lower()
                        hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        # Sort by frequency
        trending = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
        state['trending_hashtags'] = [f"#{tag}" for tag, _ in trending[:10]]
        
        print(f"✅ Found trending hashtags: {', '.join(state['trending_hashtags'][:5])}")
        
    except Exception as e:
        state['error'] = f"Error discovering hashtags: {str(e)}"
        state['trending_hashtags'] = []
    
    return state