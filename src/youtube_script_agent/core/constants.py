"""
Global constants and configuration presets
"""

# Content configuration presets
CONTENT_CONFIGS = {
    'nfl': {
        'search_base': '(NFL OR #NFL OR #SundayFootball)',
        'schedule_day': 'monday',
        'schedule_time': '08:00',
        'video_length': '10-12',
        'tone': 'energetic and passionate',
        'engagement_threshold': 50,
        'follower_threshold': 10000,
        'competitor_channels': ['@UndisputedOnFS1', '@FirstTake', '@PatMcAfeeShow']
    },
    'nba': {
        'search_base': '(NBA OR #NBA OR #NBATwitter)',
        'schedule_day': 'daily',
        'schedule_time': '09:00',
        'video_length': '8-10',
        'tone': 'casual and entertaining',
        'engagement_threshold': 30,
        'follower_threshold': 5000,
        'competitor_channels': ['@KOT4Q', '@Jxmyhighroller']
    },
    'tech': {
        'search_base': '(tech OR #TechNews OR AI OR #AI)',
        'schedule_day': 'daily',
        'schedule_time': '10:00',
        'video_length': '12-15',
        'tone': 'informative and analytical',
        'engagement_threshold': 100,
        'follower_threshold': 20000,
        'competitor_channels': ['@mkbhd', '@TechLinked']
    },
    'politics': {
        'search_base': '(politics OR #politics OR breaking)',
        'schedule_day': 'daily',
        'schedule_time': '07:00',
        'video_length': '15-20',
        'tone': 'balanced and factual',
        'engagement_threshold': 200,
        'follower_threshold': 50000,
        'competitor_channels': ['@PhilipDeFranco']
    }
}

# Script variant templates
SCRIPT_VARIANTS = [
    {
        'name': 'Hook-Heavy',
        'description': 'Maximum engagement in first 30 seconds, fast-paced throughout',
        'approach': 'Start with the most shocking moment, rapid-fire delivery, multiple hooks'
    },
    {
        'name': 'Story-Driven',
        'description': 'Narrative arc, builds tension, emotional payoff',
        'approach': 'Build a story around the biggest moment, character-driven, emotional journey'
    },
    {
        'name': 'Analytical',
        'description': 'Deep-dive analysis, tactical breakdown, expert perspective',
        'approach': 'Start with analysis, use data/stats, expert commentary style'
    },
    {
        'name': 'Controversy-First',
        'description': 'Lead with debate, balanced takes, engagement farming',
        'approach': 'Open with controversial take, present both sides, ask viewers to comment'
    },
    {
        'name': 'Reactions-Focused',
        'description': 'Twitter reactions, fan perspectives, viral takes',
        'approach': 'Showcase best Twitter reactions, fan humor, community vibe'
    }
]

# Quality filter constants
MIN_ENGAGEMENT_RATIO = 0.001
SPAM_REPLY_THRESHOLD = 0.8
BOT_RT_MULTIPLIER = 2

# API rate limits
MAX_TWEETS_PER_REQUEST = 100
MAX_COMMENTS_PER_TWEET = 100