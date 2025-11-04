"""
Media suggestions generator for video editing
"""

from typing import Dict, List
from ..core.state import AgentState


def generate_media_suggestions(state: AgentState) -> AgentState:
    """
    Generate specific media suggestions (screenshots, clips, B-roll)
    
    Args:
        state: Current agent state with filtered_tweets and sentiment_analysis
        
    Returns:
        Updated state with media_suggestions
    """
    print("🎬 Generating media suggestions...")
    
    if state.get('error'):
        return state
    
    media_suggestions = []
    
    # Top tweets to screenshot
    for i, tweet in enumerate(state['filtered_tweets'][:10], 1):
        if tweet.get('media'):
            media_suggestions.append({
                'type': 'tweet_with_media',
                'timestamp': f"[{i*60}s]",
                'description': f"Screenshot tweet from @{tweet['author_username']} with embedded media",
                'tweet_url': tweet['tweet_url'],
                'reasoning': f"High engagement ({tweet['total_engagement']}), has visual content"
            })
        else:
            media_suggestions.append({
                'type': 'tweet_screenshot',
                'timestamp': f"[{i*60}s]",
                'description': f"Screenshot tweet from @{tweet['author_username']}",
                'tweet_url': tweet['tweet_url'],
                'reasoning': f"Top quality score ({int(tweet['quality_score'])})"
            })
    
    # Extract video clip suggestions from tweet content
    sentiment = state.get('sentiment_analysis', {})
    viral_moments = sentiment.get('viral_moments', [])
    
    for moment in viral_moments[:5]:
        media_suggestions.append({
            'type': 'video_clip',
            'timestamp': '[B-ROLL]',
            'description': f"Clip of: {moment}",
            'source': 'YouTube/NFL highlights',
            'reasoning': 'Viral moment mentioned in tweets'
        })
    
    state['media_suggestions'] = media_suggestions
    print(f"✅ Generated {len(media_suggestions)} media suggestions")
    
    return state