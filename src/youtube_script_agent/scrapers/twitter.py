"""
Enhanced Twitter/X scraping with media and engagement metrics
"""

import tweepy
from datetime import datetime, timedelta
from typing import Dict, List
from ..core.state import AgentState


def scrape_enhanced_tweets(state: AgentState, twitter_client: tweepy.Client) -> AgentState:
    """
    Enhanced tweet scraping with trending hashtags, media, and full metrics
    
    Args:
        state: Current agent state with trending_hashtags
        twitter_client: Authenticated Twitter client
        
    Returns:
        Updated state with raw_tweets
    """
    print("🔍 Scraping tweets with enhanced filters...")
    
    if state.get('error'):
        return state
    
    try:
        config = state['config']
        now = datetime.utcnow()
        start_time = now - timedelta(hours=24)
        
        # Build enhanced query with trending hashtags
        base_query = config['search_base']
        if state['trending_hashtags']:
            hashtag_query = ' OR '.join(state['trending_hashtags'][:5])
            query = f"({base_query} OR {hashtag_query}) -is:retweet lang:en"
        else:
            query = f"{base_query} -is:retweet lang:en"
        
        tweets = twitter_client.search_recent_tweets(
            query=query,
            start_time=start_time.isoformat() + "Z",
            max_results=100,
            tweet_fields=['public_metrics', 'created_at', 'author_id', 'conversation_id', 'entities'],
            user_fields=['verified', 'public_metrics', 'username', 'profile_image_url'],
            expansions=['author_id', 'attachments.media_keys'],
            media_fields=['url', 'preview_image_url']
        )
        
        if not tweets.data:
            state['error'] = "No tweets found"
            return state
        
        users_dict = {user.id: user for user in tweets.includes.get('users', [])}
        media_dict = {}
        if tweets.includes and 'media' in tweets.includes:
            media_dict = {media.media_key: media for media in tweets.includes['media']}
        
        raw_tweets = []
        for tweet in tweets.data:
            author = users_dict.get(tweet.author_id)
            metrics = tweet.public_metrics
            total_engagement = metrics['like_count'] + metrics['retweet_count'] + metrics['reply_count']
            
            # Extract media URLs
            media_urls = []
            if tweet.attachments and 'media_keys' in tweet.attachments:
                for key in tweet.attachments['media_keys']:
                    if key in media_dict:
                        media = media_dict[key]
                        media_urls.append({
                            'type': media.type,
                            'url': getattr(media, 'url', None) or getattr(media, 'preview_image_url', None)
                        })
            
            # Extract URLs from tweet
            tweet_urls = []
            if tweet.entities and 'urls' in tweet.entities:
                tweet_urls = [url['expanded_url'] for url in tweet.entities['urls']]
            
            raw_tweets.append({
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at.isoformat(),
                'author_username': author.username if author else 'unknown',
                'author_verified': author.verified if author else False,
                'author_followers': author.public_metrics['followers_count'] if author else 0,
                'author_profile_image': author.profile_image_url if author else None,
                'likes': metrics['like_count'],
                'retweets': metrics['retweet_count'],
                'replies': metrics['reply_count'],
                'quotes': metrics['quote_count'],
                'total_engagement': total_engagement,
                'engagement_ratio': total_engagement / max(author.public_metrics['followers_count'], 1) if author else 0,
                'conversation_id': tweet.conversation_id,
                'media': media_urls,
                'urls': tweet_urls,
                'tweet_url': f"https://twitter.com/{author.username}/status/{tweet.id}" if author else None
            })
        
        state['raw_tweets'] = sorted(raw_tweets, key=lambda x: x['total_engagement'], reverse=True)
        print(f"✅ Scraped {len(raw_tweets)} tweets with media and URLs")
        
    except Exception as e:
        state['error'] = f"Error scraping tweets: {str(e)}"
    
    return state