"""
Agent execution and scheduling
"""

import os
import schedule
import time
import tweepy
from datetime import datetime
from langchain_anthropic import ChatAnthropic
from typing import Dict, List, Optional

from ..core.config import AgentConfig
from ..core.state import create_initial_state
from .workflow import build_agent


def run_agent_for_topic(
    topic: str, 
    config: AgentConfig, 
    custom_config: Optional[Dict] = None
) -> Dict:
    """
    Run the agent for a specific topic
    
    Args:
        topic: Topic name (e.g., 'nfl', 'nba')
        config: Agent configuration
        custom_config: Optional custom configuration overrides
        
    Returns:
        Final agent state
    """
    print(f"\n{'='*80}")
    print(f"🚀 Starting YouTube Script Generator for: {topic.upper()}")
    print(f"{'='*80}\n")
    
    # Get topic configuration
    topic_config = config.get_topic_config(topic)
    topic_config_dict = topic_config.__dict__.copy()
    
    # Apply custom overrides
    if custom_config:
        topic_config_dict.update(custom_config)
    
    # Initialize API clients
    twitter_client = tweepy.Client(bearer_token=config.api.twitter_bearer_token)
    llm = ChatAnthropic(
        model=config.claude_model,
        api_key=config.api.anthropic_api_key
    )
    
    # Build and run agent
    agent = build_agent(twitter_client, llm)
    
    # Initialize state
    initial_state = create_initial_state(topic, topic_config_dict)
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    # Display results
    if final_state.get('error'):
        print(f"\n❌ Error: {final_state['error']}")
        return None
    
    print("\n" + "="*80)
    print("📊 EXECUTION SUMMARY")
    print("="*80)
    
    print(f"\n✅ Tweets Analyzed: {len(final_state['raw_tweets'])}")
    print(f"✅ Quality Tweets: {len(final_state['filtered_tweets'])}")
    print(f"✅ Trending Hashtags: {', '.join(final_state['trending_hashtags'][:5])}")
    print(f"✅ Script Variants Generated: {len(final_state['script_variants'])}")
    print(f"✅ Media Suggestions: {len(final_state['media_suggestions'])}")
    print(f"✅ Claims Fact-Checked: {len(final_state['fact_check_results'])}")
    
    print("\n📈 TOP TRENDING TOPICS:")
    for i, topic_item in enumerate(final_state['trending_topics'][:5], 1):
        print(f"  {i}. {topic_item}")
    
    print("\n🎬 SCRIPT VARIANTS:")
    for variant in final_state['script_variants']:
        print(f"  • {variant['variant_name']}: {variant['word_count']} words")
    
    print("\n🎯 COMPETITOR INSIGHTS:")
    comp = final_state['competitor_analysis']
    if comp.get('unique_angles'):
        print("  Unique Angles (not covered by competitors):")
        for angle in comp['unique_angles'][:3]:
            print(f"    - {angle}")
    
    print("\n" + "="*80)
    print("✅ COMPLETE! Check outputs folder for all files.")
    print("="*80 + "\n")
    
    return final_state


def scheduled_job(topic: str, config: AgentConfig):
    """
    Job to run on schedule
    
    Args:
        topic: Topic to run
        config: Agent configuration
    """
    print(f"\n⏰ Scheduled job triggered for {topic} at {datetime.now()}")
    run_agent_for_topic(topic, config)


def setup_automation(topics: List[str], config: AgentConfig):
    """
    Set up automated scheduling for multiple topics
    
    Args:
        topics: List of topics to automate
        config: Agent configuration
    """
    print("\n🤖 SETTING UP AUTOMATION")
    print("="*80)
    
    for topic in topics:
        try:
            topic_config = config.get_topic_config(topic)
        except ValueError:
            print(f"⚠️ No config found for {topic}, skipping...")
            continue
        
        schedule_day = topic_config.schedule_day
        schedule_time = topic_config.schedule_time
        
        if schedule_day == 'daily':
            schedule.every().day.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Daily at {schedule_time}")
        elif schedule_day == 'monday':
            schedule.every().monday.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Every Monday at {schedule_time}")
        elif schedule_day == 'tuesday':
            schedule.every().tuesday.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Every Tuesday at {schedule_time}")
        elif schedule_day == 'wednesday':
            schedule.every().wednesday.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Every Wednesday at {schedule_time}")
        elif schedule_day == 'thursday':
            schedule.every().thursday.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Every Thursday at {schedule_time}")
        elif schedule_day == 'friday':
            schedule.every().friday.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Every Friday at {schedule_time}")
        elif schedule_day == 'saturday':
            schedule.every().saturday.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Every Saturday at {schedule_time}")
        elif schedule_day == 'sunday':
            schedule.every().sunday.at(schedule_time).do(scheduled_job, topic=topic, config=config)
            print(f"✅ {topic.upper()}: Every Sunday at {schedule_time}")
    
    print("\n🔄 Automation active. Press Ctrl+C to stop.\n")
    
    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute