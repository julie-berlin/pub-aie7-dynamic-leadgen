"""
Cached Data Loader for Survey Operations

Provides cached versions of frequently accessed data like questions,
client info, and form configurations to improve performance.
"""

import json
import logging
from typing import Dict, List, Any, Optional
import time
from functools import wraps

from .async_operations import cache, TTLCache

logger = logging.getLogger(__name__)

class CachedDataLoader:
    """Cached data loader with automatic cache management"""
    
    def __init__(self):
        # Separate caches for different data types with appropriate TTLs
        self.questions_cache = TTLCache(default_ttl=1800.0)  # 30 minutes
        self.client_cache = TTLCache(default_ttl=3600.0)    # 1 hour
        self.form_cache = TTLCache(default_ttl=1800.0)      # 30 minutes
        
        # Statistics
        self.stats = {
            'questions_hits': 0,
            'questions_misses': 0,
            'client_hits': 0,
            'client_misses': 0,
            'form_hits': 0,
            'form_misses': 0
        }
    
    def get_questions(self, form_id: str, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get questions for a form with caching.
        
        Args:
            form_id: Form identifier
            force_refresh: Force cache refresh
            
        Returns:
            List of question dictionaries
        """
        cache_key = f"questions_{form_id}"
        
        if not force_refresh:
            cached_questions = self.questions_cache.get(cache_key)
            if cached_questions is not None:
                self.stats['questions_hits'] += 1
                logger.debug(f"Cache hit for questions: {form_id}")
                return cached_questions
        
        self.stats['questions_misses'] += 1
        logger.debug(f"Cache miss for questions: {form_id}, loading from database")
        
        try:
            # Load from database/tools
            from ..tools import load_questions
            
            questions_json = load_questions.invoke({'form_id': form_id})
            questions = json.loads(questions_json) if questions_json else []
            
            # Cache the result
            self.questions_cache.set(cache_key, questions)
            
            logger.info(f"Loaded and cached {len(questions)} questions for form {form_id}")
            return questions
            
        except Exception as e:
            logger.error(f"Failed to load questions for {form_id}: {e}")
            return []
    
    def get_client_info(self, form_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get client info for a form with caching.
        
        Args:
            form_id: Form identifier
            force_refresh: Force cache refresh
            
        Returns:
            Client info dictionary
        """
        cache_key = f"client_{form_id}"
        
        if not force_refresh:
            cached_client = self.client_cache.get(cache_key)
            if cached_client is not None:
                self.stats['client_hits'] += 1
                logger.debug(f"Cache hit for client info: {form_id}")
                return cached_client
        
        self.stats['client_misses'] += 1
        logger.debug(f"Cache miss for client info: {form_id}, loading from database")
        
        try:
            # Load from database/tools
            from ..tools import load_client_info
            
            client_json = load_client_info.invoke({'form_id': form_id})
            client_info = json.loads(client_json) if client_json else {}
            
            # Cache the result
            self.client_cache.set(cache_key, client_info)
            
            logger.info(f"Loaded and cached client info for form {form_id}")
            return client_info
            
        except Exception as e:
            logger.error(f"Failed to load client info for {form_id}: {e}")
            return {}
    
    def get_form_config(self, form_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get form configuration with caching.
        
        Args:
            form_id: Form identifier  
            force_refresh: Force cache refresh
            
        Returns:
            Form configuration dictionary
        """
        cache_key = f"form_{form_id}"
        
        if not force_refresh:
            cached_form = self.form_cache.get(cache_key)
            if cached_form is not None:
                self.stats['form_hits'] += 1
                logger.debug(f"Cache hit for form config: {form_id}")
                return cached_form
        
        self.stats['form_misses'] += 1
        logger.debug(f"Cache miss for form config: {form_id}, loading from database")
        
        try:
            # Load from database
            from ..database import db
            
            form_config = db.get_form(form_id)
            if not form_config:
                form_config = {}
            
            # Cache the result
            self.form_cache.set(cache_key, form_config)
            
            logger.info(f"Loaded and cached form config for {form_id}")
            return form_config
            
        except Exception as e:
            logger.error(f"Failed to load form config for {form_id}: {e}")
            return {}
    
    def invalidate_form_data(self, form_id: str) -> None:
        """
        Invalidate all cached data for a specific form.
        
        Args:
            form_id: Form identifier to invalidate
        """
        # Remove from all caches
        for cache_instance, prefix in [
            (self.questions_cache, "questions_"),
            (self.client_cache, "client_"),
            (self.form_cache, "form_")
        ]:
            cache_key = f"{prefix}{form_id}"
            if cache_key in cache_instance.cache:
                del cache_instance.cache[cache_key]
        
        logger.info(f"Invalidated all cached data for form {form_id}")
    
    def preload_form_data(self, form_id: str) -> Dict[str, Any]:
        """
        Preload all data for a form to warm the cache.
        
        Args:
            form_id: Form identifier
            
        Returns:
            Dictionary with all preloaded data
        """
        logger.info(f"Preloading data for form {form_id}")
        
        start_time = time.time()
        
        # Load all data in parallel would be ideal, but for now sequential
        questions = self.get_questions(form_id)
        client_info = self.get_client_info(form_id)
        form_config = self.get_form_config(form_id)
        
        duration = (time.time() - start_time) * 1000
        
        logger.info(
            f"Preloaded form data for {form_id} in {duration:.2f}ms: "
            f"{len(questions)} questions, client_info: {bool(client_info)}, "
            f"form_config: {bool(form_config)}"
        )
        
        return {
            'questions': questions,
            'client_info': client_info,
            'form_config': form_config
        }
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_hits = self.stats['questions_hits'] + self.stats['client_hits'] + self.stats['form_hits']
        total_misses = self.stats['questions_misses'] + self.stats['client_misses'] + self.stats['form_misses']
        total_requests = total_hits + total_misses
        
        hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_requests': total_requests,
            'total_hits': total_hits,
            'total_misses': total_misses,
            'hit_rate_percent': round(hit_rate, 2),
            'questions_hits': self.stats['questions_hits'],
            'questions_misses': self.stats['questions_misses'],
            'client_hits': self.stats['client_hits'],
            'client_misses': self.stats['client_misses'],
            'form_hits': self.stats['form_hits'],
            'form_misses': self.stats['form_misses']
        }
    
    def clear_all_caches(self) -> None:
        """Clear all caches"""
        self.questions_cache.clear()
        self.client_cache.clear()
        self.form_cache.clear()
        
        # Reset stats
        for key in self.stats:
            self.stats[key] = 0
        
        logger.info("Cleared all data caches")
    
    def cleanup_expired(self) -> int:
        """Clean up expired cache entries and return total removed"""
        questions_removed = self.questions_cache.cleanup_expired()
        client_removed = self.client_cache.cleanup_expired()
        form_removed = self.form_cache.cleanup_expired()
        
        total_removed = questions_removed + client_removed + form_removed
        
        if total_removed > 0:
            logger.info(f"Cleaned up {total_removed} expired cache entries")
        
        return total_removed

# Global instance
data_loader = CachedDataLoader()

# Convenience functions that match the tool interface

def load_questions_cached(form_id: str, force_refresh: bool = False) -> str:
    """
    Load questions with caching - matches the tool interface.
    
    Returns JSON string to match existing tool behavior.
    """
    questions = data_loader.get_questions(form_id, force_refresh)
    return json.dumps(questions)

def load_client_info_cached(form_id: str, force_refresh: bool = False) -> str:
    """
    Load client info with caching - matches the tool interface.
    
    Returns JSON string to match existing tool behavior.
    """
    client_info = data_loader.get_client_info(form_id, force_refresh)
    return json.dumps(client_info)

def load_form_config_cached(form_id: str, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Load form config with caching.
    
    Returns dictionary directly.
    """
    return data_loader.get_form_config(form_id, force_refresh)

# Cache warming functions

def warm_cache_for_form(form_id: str) -> None:
    """Warm cache for a specific form"""
    data_loader.preload_form_data(form_id)

def warm_cache_for_active_forms() -> None:
    """Warm cache for all currently active forms"""
    try:
        from ..database import db
        
        # Get active forms (forms with recent sessions)
        active_forms = db.get_active_forms(days_back=7)
        
        for form_id in active_forms:
            warm_cache_for_form(form_id)
            
        logger.info(f"Warmed cache for {len(active_forms)} active forms")
        
    except Exception as e:
        logger.error(f"Failed to warm cache for active forms: {e}")

# Decorator for automatic caching

def with_form_data_cache(cache_questions: bool = True, cache_client: bool = True, cache_form: bool = True):
    """
    Decorator that automatically provides cached form data to functions.
    
    The decorated function will receive additional keyword arguments:
    - cached_questions: List of questions (if cache_questions=True)
    - cached_client_info: Client info dict (if cache_client=True) 
    - cached_form_config: Form config dict (if cache_form=True)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Try to extract form_id from args or kwargs
            form_id = kwargs.get('form_id')
            
            if not form_id and args:
                # Try to extract from state if first arg is state dict
                state = args[0]
                if isinstance(state, dict) and 'core' in state:
                    form_id = state['core'].get('form_id')
                elif isinstance(state, dict) and 'form_id' in state:
                    form_id = state['form_id']
            
            if form_id:
                # Add cached data to kwargs
                if cache_questions:
                    kwargs['cached_questions'] = data_loader.get_questions(form_id)
                if cache_client:
                    kwargs['cached_client_info'] = data_loader.get_client_info(form_id)
                if cache_form:
                    kwargs['cached_form_config'] = data_loader.get_form_config(form_id)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Export main components
__all__ = [
    'CachedDataLoader',
    'data_loader',
    'load_questions_cached',
    'load_client_info_cached', 
    'load_form_config_cached',
    'warm_cache_for_form',
    'warm_cache_for_active_forms',
    'with_form_data_cache'
]