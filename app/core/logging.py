from loguru import logger
import sys
import json
from pathlib import Path
from app.core.config import settings

def setup_logging():
    # Remove default logger
    logger.remove()
    
    # Configure JSON logging
    log_format = {
        "time": "{time:YYYY-MM-DD HH:mm:ss.SSS}",
        "level": "{level}",
        "request_id": "{extra[request_id]}",
        "message": "{message}",
        "extra": "{extra}"
    }
    
    # Console handler for development
    logger.add(
        sys.stdout,
        format=lambda record: json.dumps(log_format),
        level="DEBUG" if settings.DEBUG else "INFO",
        serialize=True
    )
    
    # File handler for production
    log_path = Path("logs/audiov4.log")
    log_path.parent.mkdir(exist_ok=True)
    
    logger.add(
        log_path,
        rotation="500 MB",
        retention="10 days",
        format=lambda record: json.dumps(log_format),
        level="DEBUG",
        serialize=True
    )
    
    return logger
