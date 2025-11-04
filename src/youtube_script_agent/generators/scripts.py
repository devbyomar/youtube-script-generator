"""
Script generation with multiple variants
"""

import json
from langchain_core.messages import HumanMessage
from typing import Dict, List
from ..core.state import AgentState
from ..core.constants import SCRIPT_VARIANTS


def generate_multiple_script_variants(state: AgentState, llm) -> AgentState:
    """
    Generate 3-5 different script variations
    
    Args:
        state: Current agent state with all analysis complete
        llm: Claude LLM instance
        
    Returns:
        Updated state with script_variants
    """
    print("📝 Generating multiple script variants...")
    
    if state.get('error'):
        return state
    
    config = state['config']
    sentiment = state.get('sentiment_analysis', {})
    competitor_analysis = state.get('competitor_analysis', {})
    media_suggestions = state.get('media_suggestions', [])
    
    # Context for all variants
    context = f"""
TOPIC: {state['topic']}
TONE: {config['tone']}
VIDEO LENGTH: {config['video_length']} minutes
TRENDING HASHTAGS: {', '.join(state['trending_hashtags'][:5])}
SENTIMENT: {sentiment.get('sentiment', 'N/A')}
TRENDING TOPICS: {', '.join(sentiment.get('trending_topics', [])[:5])}
VIRAL MOMENTS: {', '.join(sentiment.get('viral_moments', [])[:3])}
UNIQUE ANGLES (vs competitors): {', '.join(competitor_analysis.get('unique_angles', [])[:3])}

TOP TWEETS:
{json.dumps([{'author': t['author_username'], 'text': t['text'][:100], 'engagement': t['total_engagement']} for t in state['filtered_tweets'][:5]], indent=2)}

MEDIA SUGGESTIONS:
{json.dumps(media_suggestions[:10], indent=2)}
"""
    
    script_variants = []
    
    for variant in SCRIPT_VARIANTS[:3]:  # Generate top 3 variants
        print(f"  → Generating {variant['name']} variant...")
        
        prompt = f"""{context}

VARIANT: {variant['name']}
DESCRIPTION: {variant['description']}
APPROACH: {variant['approach']}

Write a COMPLETE YouTube script for a {config['video_length']} minute video.

Requirements:
- Match the {config['tone']} tone
- Use the variant approach described above
- Include [TIMESTAMP X:XX] markers every major section
- Add [SCREENSHOT: tweet_url] for specific tweets to show
- Include [B-ROLL: description] for visual suggestions
- Add [PAUSE] for emphasis
- Reference fact-checked claims safely (from fact-check data)
- Strong CTA at end
- Word count: {int(config['video_length'].split('-')[0]) * 150}-{int(config['video_length'].split('-')[1]) * 150} words

Start naturally and make it {variant['description'].lower()}."""
        
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            
            script_variants.append({
                'variant_name': variant['name'],
                'description': variant['description'],
                'script': response.content,
                'word_count': len(response.content.split())
            })
            
        except Exception as e:
            print(f"⚠️ Error generating {variant['name']}: {e}")
    
    state['script_variants'] = script_variants
    print(f"✅ Generated {len(script_variants)} script variants")
    
    return state