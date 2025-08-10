"""
Async Utilities for Fire-and-Forget Operations

Provides non-blocking database and external service operations
to optimize graph execution performance.
"""

import asyncio
import logging
from typing import Callable, Any, Dict, Optional, List
from functools import wraps
import time
from concurrent.futures import ThreadPoolExecutor
import threading

logger = logging.getLogger(__name__)

# Global thread pool for fire-and-forget operations
_thread_pool: Optional[ThreadPoolExecutor] = None
_thread_pool_lock = threading.Lock()

def get_thread_pool() -> ThreadPoolExecutor:
    """Get or create the global thread pool for async operations"""
    global _thread_pool
    
    with _thread_pool_lock:
        if _thread_pool is None:
            _thread_pool = ThreadPoolExecutor(
                max_workers=10,
                thread_name_prefix="survey_async_"
            )
    
    return _thread_pool

def fire_and_forget(func: Callable) -> Callable:
    """
    Decorator to make a function fire-and-forget (non-blocking).
    
    The function will be executed in a background thread and any
    exceptions will be logged but not raised.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        def background_task():
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                
                logger.debug(
                    f"Fire-and-forget operation completed: {func.__name__} in {duration:.2f}ms",
                    extra={
                        "operation": func.__name__,
                        "duration_ms": duration,
                        "success": True
                    }
                )
                return result
                
            except Exception as e:
                logger.error(
                    f"Fire-and-forget operation failed: {func.__name__}: {e}",
                    extra={
                        "operation": func.__name__,
                        "error": str(e),
                        "success": False
                    }
                )
        
        # Submit to thread pool
        thread_pool = get_thread_pool()
        future = thread_pool.submit(background_task)
        
        # Don't wait for result - truly fire and forget
        return None
    
    return wrapper

async def fire_and_forget_async(coro_func: Callable, *args, **kwargs):
    """
    Execute an async function in a fire-and-forget manner.
    
    Args:
        coro_func: Async function to execute
        *args: Arguments for the function
        **kwargs: Keyword arguments for the function
    """
    async def background_task():
        try:
            start_time = time.time()
            result = await coro_func(*args, **kwargs)
            duration = (time.time() - start_time) * 1000
            
            logger.debug(
                f"Async fire-and-forget completed: {coro_func.__name__} in {duration:.2f}ms",
                extra={
                    "operation": coro_func.__name__,
                    "duration_ms": duration,
                    "success": True
                }
            )
            return result
            
        except Exception as e:
            logger.error(
                f"Async fire-and-forget failed: {coro_func.__name__}: {e}",
                extra={
                    "operation": coro_func.__name__,
                    "error": str(e),
                    "success": False
                }
            )
    
    # Create task and don't wait for it
    asyncio.create_task(background_task())

# Database operation utilities

class AsyncDatabaseOps:
    """Fire-and-forget database operations for performance optimization"""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
    
    @fire_and_forget
    def save_tracking_data(self, session_id: str, tracking_data: Dict[str, Any]):
        """Save tracking data without blocking graph execution"""
        try:
            if self.db:
                self.db.save_tracking_data(session_id, tracking_data)
            else:
                # Import here to avoid circular dependencies
                from ..database import db
                db.save_tracking_data(session_id, tracking_data)
                
        except Exception as e:
            logger.error(f"Failed to save tracking data for {session_id}: {e}")
    
    @fire_and_forget  
    def save_response_batch(self, session_id: str, responses: List[Dict[str, Any]]):
        """Save multiple responses without blocking"""
        try:
            if self.db:
                for response in responses:
                    self.db.save_response(session_id, response)
            else:
                from ..database import db
                for response in responses:
                    db.save_response(session_id, response)
                    
        except Exception as e:
            logger.error(f"Failed to save response batch for {session_id}: {e}")
    
    @fire_and_forget
    def update_session_state(self, session_id: str, state_data: Dict[str, Any]):
        """Update session state without blocking"""
        try:
            if self.db:
                self.db.update_session(session_id, state_data)
            else:
                from ..database import db
                db.update_session(session_id, state_data)
                
        except Exception as e:
            logger.error(f"Failed to update session state for {session_id}: {e}")
    
    @fire_and_forget
    def save_completion_data(self, session_id: str, completion_data: Dict[str, Any]):
        """Save completion data without blocking"""
        try:
            if self.db:
                self.db.save_completion(session_id, completion_data)
            else:
                from ..database import db
                db.save_completion(session_id, completion_data)
                
        except Exception as e:
            logger.error(f"Failed to save completion data for {session_id}: {e}")

# Batch operations for efficiency

class BatchOperationManager:
    """Manages batched operations to reduce database load"""
    
    def __init__(self, batch_size: int = 10, flush_interval: float = 5.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.pending_operations: List[Dict[str, Any]] = []
        self.last_flush = time.time()
        self._lock = threading.Lock()
    
    def add_operation(self, operation_type: str, data: Dict[str, Any]):
        """Add operation to batch"""
        with self._lock:
            self.pending_operations.append({
                'type': operation_type,
                'data': data,
                'timestamp': time.time()
            })
            
            # Check if we should flush
            if (len(self.pending_operations) >= self.batch_size or
                time.time() - self.last_flush >= self.flush_interval):
                self._flush_operations()
    
    @fire_and_forget
    def _flush_operations(self):
        """Flush pending operations to database"""
        with self._lock:
            if not self.pending_operations:
                return
            
            operations_to_process = self.pending_operations.copy()
            self.pending_operations.clear()
            self.last_flush = time.time()
        
        try:
            from ..database import db
            
            # Group operations by type for efficiency
            grouped_ops = {}
            for op in operations_to_process:
                op_type = op['type']
                if op_type not in grouped_ops:
                    grouped_ops[op_type] = []
                grouped_ops[op_type].append(op['data'])
            
            # Execute batched operations
            for op_type, data_list in grouped_ops.items():
                if op_type == 'save_response':
                    db.save_response_batch(data_list)
                elif op_type == 'update_session':
                    db.update_session_batch(data_list)
                elif op_type == 'save_tracking':
                    db.save_tracking_batch(data_list)
                    
            logger.info(f"Flushed {len(operations_to_process)} batched operations")
            
        except Exception as e:
            logger.error(f"Failed to flush batched operations: {e}")

# Parallel execution utilities

async def run_parallel_non_blocking(tasks: List[Callable], timeout: float = 30.0):
    """
    Run multiple tasks in parallel without blocking on any single task.
    
    Args:
        tasks: List of callable functions or coroutines
        timeout: Maximum time to wait for all tasks
        
    Returns:
        List of results (None for failed tasks)
    """
    async def safe_task_wrapper(task):
        try:
            if asyncio.iscoroutinefunction(task):
                return await task()
            else:
                # Run sync function in thread pool
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(get_thread_pool(), task)
        except Exception as e:
            logger.error(f"Parallel task failed: {e}")
            return None
    
    # Create tasks
    async_tasks = [safe_task_wrapper(task) for task in tasks]
    
    try:
        # Wait for all tasks with timeout
        results = await asyncio.wait_for(
            asyncio.gather(*async_tasks, return_exceptions=True),
            timeout=timeout
        )
        
        # Filter out exceptions
        return [r for r in results if not isinstance(r, Exception)]
        
    except asyncio.TimeoutError:
        logger.warning(f"Parallel execution timed out after {timeout}s")
        return []

# Caching utilities for performance

class TTLCache:
    """Simple TTL (Time To Live) cache for expensive operations"""
    
    def __init__(self, default_ttl: float = 300.0):  # 5 minutes default
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache if not expired"""
        with self._lock:
            if key not in self.cache:
                return None
                
            item = self.cache[key]
            if time.time() > item['expires_at']:
                del self.cache[key]
                return None
                
            return item['value']
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set item in cache with TTL"""
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        
        with self._lock:
            self.cache[key] = {
                'value': value,
                'expires_at': expires_at
            }
    
    def clear(self) -> None:
        """Clear entire cache"""
        with self._lock:
            self.cache.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired items and return count removed"""
        now = time.time()
        expired_keys = []
        
        with self._lock:
            for key, item in self.cache.items():
                if now > item['expires_at']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
        
        return len(expired_keys)

# Global instances
async_db = AsyncDatabaseOps()
batch_manager = BatchOperationManager()
cache = TTLCache()

# Cleanup function
def cleanup_resources():
    """Clean up resources on shutdown"""
    global _thread_pool
    
    if _thread_pool:
        _thread_pool.shutdown(wait=True)
        _thread_pool = None
    
    cache.clear()

# Export main components
__all__ = [
    'fire_and_forget',
    'fire_and_forget_async',
    'AsyncDatabaseOps',
    'BatchOperationManager',
    'TTLCache',
    'run_parallel_non_blocking',
    'async_db',
    'batch_manager',
    'cache',
    'cleanup_resources'
]