import logging
import logging.config
import sys
from typing import Dict, Any
from .settings import settings


def configure_logging() -> None:
    """Configure structured logging for the FastAPI application"""
    
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(funcName)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(pathname)s %(lineno)d %(funcName)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "default",
                "stream": sys.stdout,
            },
            "detailed_console": {
                "class": "logging.StreamHandler", 
                "level": "DEBUG",
                "formatter": "detailed",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "": {
                "level": settings.log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            "app": {
                "level": settings.log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            "app.services": {
                "level": settings.log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            "app.api": {
                "level": settings.log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }
    
    # Enable detailed logging in debug mode
    if settings.debug:
        logging_config["loggers"][""]["handlers"] = ["detailed_console"]
        logging_config["loggers"]["app"]["handlers"] = ["detailed_console"]
        logging_config["loggers"]["app.services"]["handlers"] = ["detailed_console"]
        logging_config["loggers"]["app.api"]["handlers"] = ["detailed_console"]
    
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    return logging.getLogger(name)