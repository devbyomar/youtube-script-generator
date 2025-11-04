"""
Comment thread scraping for sentiment analysis
"""

import tweepy
from typing import Dict, List
from ..core.state import AgentState


def scrape_comments_detailed(state: AgentState, twitter_client: tweepy.Client) -> AgentState:
    """
    Enhanced comment scraping for top tweets
    
    Args:
        state: Current agent state with filtered_tweets
        twitter_client: Authenticated Twitter client
        
    Returns:
        Updated state with comments added to tweets
    """
    print("💬 Scraping detailed comment threads...")
    
    if state.get('error') or not state['filtered_tweets']:
        return state
    
    top_tweets = state['filtered_tweets'][:15]
    
    for tweet in top_tweets:
        try:
            conversation_tweets = twitter_client.search_recent_tweets(
                query=f"conversation_id:{tweet['conversation_id']}",
                max_results=100,
                tweet_fields=['public_metrics', 'created_at', 'author_id'],
                user_fields=['username', 'verified']
            )
            
            if conversation_tweets.data:
                comments = []
                for t in conversation_tweets.data:
                    comments.append({
                        'text': t.text,
                        'likes': t.public_metrics['like_count'],
                        'created_at': t.created_at.isoformat()
                    })
                
                tweet['comments'] = sorted(comments, key=lambda x: x['likes'], reverse=True)[:30]
                tweet['comment_count'] = len(comments)
        
        except Exception as e:
            tweet['comments'] = []
            tweet['comment_count'] = 0
    
    state['filtered_tweets'] = top_tweets
    print("✅ Detailed comments scraped")
    
    return state