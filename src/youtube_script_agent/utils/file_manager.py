"""
File I/O operations and output management
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from ..core.state import AgentState


def compile_final_output(state: AgentState) -> AgentState:
    """
    Compile everything into final deliverable package
    
    Args:
        state: Current agent state with all analysis complete
        
    Returns:
        Updated state with final_output
    """
    print("📦 Compiling final output package...")
    
    if state.get('error'):
        return state
    
    final_output = {
        'metadata': {
            'topic': state['topic'],
            'generated_at': datetime.utcnow().isoformat(),
            'config': state['config'],
            'trending_hashtags': state['trending_hashtags']
        },
        'analysis': {
            'tweets_analyzed': len(state['raw_tweets']),
            'quality_tweets': len(state['filtered_tweets']),
            'sentiment': state['sentiment_analysis'],
            'competitor_insights': state['competitor_analysis'],
            'fact_checks': state['fact_check_results']
        },
        'content': {
            'script_variants': state['script_variants'],
            'media_suggestions': state['media_suggestions'],
            'top_tweets': state['filtered_tweets'][:20]
        },
        'recommendations': {
            'best_variant': state['script_variants'][0]['variant_name'] if state['script_variants'] else None,
            'key_talking_points': state['sentiment_analysis'].get('trending_topics', [])[:5],
            'unique_angles': state['competitor_analysis'].get('unique_angles', [])
        }
    }
    
    state['final_output'] = final_output
    print("✅ Final output compiled")
    
    return state


def save_outputs(state: AgentState) -> AgentState:
    """
    Save all outputs to organized files
    
    Args:
        state: Current agent state with final_output
        
    Returns:
        Updated state (unchanged)
    """
    print("💾 Saving outputs...")
    
    if state.get('error'):
        return state
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(f"outputs/{state['topic']}_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save each script variant
    for i, variant in enumerate(state['script_variants'], 1):
        script_file = output_dir / f"script_{i}_{variant['variant_name'].lower().replace(' ', '_').replace('-', '_')}.txt"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {variant['variant_name']} Variant ===\n")
            f.write(f"{variant['description']}\n")
            f.write(f"Word Count: {variant['word_count']}\n\n")
            f.write(variant['script'])
        print(f"  ✓ Saved {variant['variant_name']} script")
    
    # Save media suggestions
    media_file = output_dir / "media_suggestions.json"
    with open(media_file, 'w', encoding='utf-8') as f:
        json.dump(state['media_suggestions'], f, indent=2)
    print(f"  ✓ Saved media suggestions")
    
    # Save analysis summary
    analysis_file = output_dir / "analysis_summary.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(state['final_output'], f, indent=2)
    print(f"  ✓ Saved analysis summary")
    
    # Save top tweets with links
    tweets_file = output_dir / "top_tweets.txt"
    with open(tweets_file, 'w', encoding='utf-8') as f:
        f.write("=== TOP 20 TWEETS TO REFERENCE ===\n\n")
        for i, tweet in enumerate(state['filtered_tweets'][:20], 1):
            f.write(f"{i}. @{tweet['author_username']} ({tweet['total_engagement']} engagement)\n")
            f.write(f"   {tweet['text']}\n")
            f.write(f"   {tweet['tweet_url']}\n")
            if tweet.get('fact_check'):
                f.write(f"   ⚠️ FACT-CHECK: {tweet['fact_check'].get('recommendation', 'N/A')}\n")
            f.write("\n")
    print(f"  ✓ Saved top tweets")
    
    # Create comparison summary
    comparison_file = output_dir / "variant_comparison.txt"
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write("=== SCRIPT VARIANT COMPARISON ===\n\n")
        for variant in state['script_variants']:
            f.write(f"## {variant['variant_name']}\n")
            f.write(f"Description: {variant['description']}\n")
            f.write(f"Word Count: {variant['word_count']}\n")
            f.write(f"Best For: {variant.get('best_for', 'General audience')}\n\n")
    print(f"  ✓ Saved variant comparison")
    
    print(f"\n✅ All outputs saved to: {output_dir}")
    
    return state