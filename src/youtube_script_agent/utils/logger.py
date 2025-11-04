"""
Logging configuration
"""

import logging
from rich.logging import RichHandler


def setup_logger(name: str = "youtube_script_agent", level: int = logging.INFO) -> logging.Logger:
    """
    Setup logger with rich formatting
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Add rich handler
    handler = RichHandler(rich_tracebacks=True)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    
    return logger