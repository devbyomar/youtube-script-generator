"""
LangGraph workflow builder
"""

from langgraph.graph import StateGraph, END
import tweepy
from langchain_anthropic import ChatAnthropic

from ..core.state import AgentState
from ..scrapers.hashtags import discover_trending_hashtags
from ..scrapers.twitter import scrape_enhanced_tweets
from ..scrapers.comments import scrape_comments_detailed
from ..utils.filters import filter_quality_tweets_advanced
from ..analyzers.competitor import analyze_competitors
from ..analyzers.fact_checker import fact_check_claims
from ..analyzers.sentiment import analyze_sentiment_advanced
from ..generators.media import generate_media_suggestions
from ..generators.scripts import generate_multiple_script_variants
from ..utils.file_manager import compile_final_output, save_outputs


def build_agent(twitter_client: tweepy.Client, llm: ChatAnthropic):
    """
    Build and compile the complete LangGraph agent
    
    Args:
        twitter_client: Authenticated Twitter client
        llm: Claude LLM instance
        
    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(AgentState)
    
    # Add all nodes with their dependencies injected
    workflow.add_node("discover_hashtags", lambda state: discover_trending_hashtags(state, twitter_client))
    workflow.add_node("scrape_tweets", lambda state: scrape_enhanced_tweets(state, twitter_client))
    workflow.add_node("filter_tweets", filter_quality_tweets_advanced)
    workflow.add_node("analyze_competitors", lambda state: analyze_competitors(state, twitter_client, llm))
    workflow.add_node("scrape_comments", lambda state: scrape_comments_detailed(state, twitter_client))
    workflow.add_node("fact_check", lambda state: fact_check_claims(state, llm))
    workflow.add_node("analyze_sentiment", lambda state: analyze_sentiment_advanced(state, llm))
    workflow.add_node("generate_media", generate_media_suggestions)
    workflow.add_node("generate_scripts", lambda state: generate_multiple_script_variants(state, llm))
    workflow.add_node("compile_output", compile_final_output)
    workflow.add_node("save_files", save_outputs)
    
    # Define complete flow
    workflow.set_entry_point("discover_hashtags")
    workflow.add_edge("discover_hashtags", "scrape_tweets")
    workflow.add_edge("scrape_tweets", "filter_tweets")
    workflow.add_edge("filter_tweets", "analyze_competitors")
    workflow.add_edge("analyze_competitors", "scrape_comments")
    workflow.add_edge("scrape_comments", "fact_check")
    workflow.add_edge("fact_check", "analyze_sentiment")
    workflow.add_edge("analyze_sentiment", "generate_media")
    workflow.add_edge("generate_media", "generate_scripts")
    workflow.add_edge("generate_scripts", "compile_output")
    workflow.add_edge("compile_output", "save_files")
    workflow.add_edge("save_files", END)
    
    return workflow.compile()