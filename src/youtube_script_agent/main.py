"""
Main entry point for the CLI
"""

import argparse
from pathlib import Path
from .agents.executor import run_agent_for_topic, setup_automation
from .core.config import load_config


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Advanced YouTube Script Generator')
    parser.add_argument('--topic', type=str, default='nfl',
                       help='Topic to analyze (nfl, nba, tech, politics)')
    parser.add_argument('--automate', action='store_true',
                       help='Run in automation mode with scheduling')
    parser.add_argument('--topics', nargs='+', default=['nfl', 'nba'],
                       help='Topics to automate (space-separated)')
    parser.add_argument('--run-now', action='store_true',
                       help='Run immediately without scheduling')
    parser.add_argument('--config', type=Path,
                       help='Path to config file')

    # Custom config overrides
    parser.add_argument('--engagement-threshold', type=int,
                       help='Minimum engagement threshold')
    parser.add_argument('--follower-threshold', type=int,
                       help='Minimum follower threshold')
    parser.add_argument('--video-length', type=str,
                       help='Video length (e.g., "10-12")')
    parser.add_argument('--tone', type=str,
                       help='Video tone/style')

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Build custom config from args
    custom_config = {}
    if args.engagement_threshold:
        custom_config['engagement_threshold'] = args.engagement_threshold
    if args.follower_threshold:
        custom_config['follower_threshold'] = args.follower_threshold
    if args.video_length:
        custom_config['video_length'] = args.video_length
    if args.tone:
        custom_config['tone'] = args.tone

    # Execution modes
    if args.automate:
        setup_automation(args.topics, config)
    elif args.run_now:
        for topic in args.topics:
            run_agent_for_topic(topic, config, custom_config)
    else:
        run_agent_for_topic(args.topic, config, custom_config)


if __name__ == "__main__":
    main()