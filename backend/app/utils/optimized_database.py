"""
Optimized Database Operations with Connection Pooling

Provides connection pooling, batch operations, and performance optimizations
for the survey system database operations.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import time
from contextlib import asynccontextmanager
import threading
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import queue
import json

from .database_monitoring import monitor

logger = logging.getLogger(__name__)

@dataclass
class BatchOperation:
    """Represents a batched database operation"""
    operation_type: str
    table: str
    data: Dict[str, Any]
    timestamp: float
    callback: Optional[callable] = None

class ConnectionPool:
    """Simple connection pool for database operations"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.available_connections = queue.Queue(maxsize=max_connections)
        self.total_connections = 0
        self.lock = threading.Lock()
        self._stats = {
            'created': 0,
            'borrowed': 0,
            'returned': 0,
            'failed': 0
        }
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            # Try to get an available connection with timeout
            connection = self.available_connections.get(timeout=5.0)
            self._stats['borrowed'] += 1
            return connection
            
        except queue.Empty:
            # Create new connection if under limit
            with self.lock:
                if self.total_connections < self.max_connections:
                    connection = self._create_connection()
                    if connection:
                        self.total_connections += 1
                        self._stats['created'] += 1
                        self._stats['borrowed'] += 1
                        return connection
            
            # Wait for an available connection
            connection = self.available_connections.get()
            self._stats['borrowed'] += 1
            return connection
    
    def return_connection(self, connection):
        """Return a connection to the pool"""
        if connection:
            try:
                self.available_connections.put(connection, timeout=1.0)
                self._stats['returned'] += 1
            except queue.Full:
                # Connection pool is full, close the connection
                self._close_connection(connection)
    
    def _create_connection(self):
        """Create a new database connection"""
        try:
            from ..database import SupabaseClient
            client = SupabaseClient()
            return client
        except Exception as e:
            logger.error(f"Failed to create database connection: {e}")
            self._stats['failed'] += 1
            return None
    
    def _close_connection(self, connection):
        """Close a database connection"""
        # Supabase client doesn't need explicit closing
        with self.lock:
            self.total_connections -= 1
    
    def get_stats(self) -> Dict[str, int]:
        """Get connection pool statistics"""
        return {
            **self._stats,
            'total_connections': self.total_connections,
            'available_connections': self.available_connections.qsize(),
            'active_connections': self.total_connections - self.available_connections.qsize()
        }

class BatchProcessor:
    """Processes database operations in batches for efficiency"""
    
    def __init__(self, batch_size: int = 50, flush_interval: float = 2.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.operations: List[BatchOperation] = []
        self.lock = threading.Lock()
        self.last_flush = time.time()
        self.executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="batch_")
    
    def add_operation(self, operation: BatchOperation):
        """Add operation to batch"""
        with self.lock:
            self.operations.append(operation)
            
            # Check if we should flush
            should_flush = (
                len(self.operations) >= self.batch_size or
                time.time() - self.last_flush >= self.flush_interval
            )
            
            if should_flush:
                self._schedule_flush()
    
    def _schedule_flush(self):
        """Schedule batch flush in background"""
        if not self.operations:
            return
            
        # Get operations to process
        operations_to_process = self.operations.copy()
        self.operations.clear()
        self.last_flush = time.time()
        
        # Process in background
        self.executor.submit(self._process_batch, operations_to_process)
    
    def _process_batch(self, operations: List[BatchOperation]):
        """Process a batch of operations"""
        if not operations:
            return
        
        start_time = time.time()
        
        try:
            # Group operations by table and type
            grouped = {}
            for op in operations:
                key = f"{op.table}_{op.operation_type}"
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(op)
            
            # Process each group
            from ..database import db
            
            for group_key, group_ops in grouped.items():
                table, op_type = group_key.rsplit('_', 1)
                
                try:
                    if op_type == 'insert':
                        self._batch_insert(db, table, group_ops)
                    elif op_type == 'update':
                        self._batch_update(db, table, group_ops)
                    elif op_type == 'upsert':
                        self._batch_upsert(db, table, group_ops)
                        
                except Exception as e:
                    logger.error(f"Batch operation failed for {group_key}: {e}")
                    
                    # Execute individually as fallback
                    for op in group_ops:
                        try:
                            self._execute_single_operation(db, op)
                        except Exception as single_error:
                            logger.error(f"Single operation fallback failed: {single_error}")
            
            duration = (time.time() - start_time) * 1000
            logger.info(f"Processed batch of {len(operations)} operations in {duration:.2f}ms")
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
    
    def _batch_insert(self, db, table: str, operations: List[BatchOperation]):
        """Execute batch insert operations"""
        data_list = [op.data for op in operations]
        
        if table == 'responses':
            db.client.table('responses').insert(data_list).execute()
        elif table == 'tracking_data':
            db.client.table('tracking_data').insert(data_list).execute()
        elif table == 'lead_sessions':
            db.client.table('lead_sessions').insert(data_list).execute()
        else:
            # Generic insert
            db.client.table(table).insert(data_list).execute()
    
    def _batch_update(self, db, table: str, operations: List[BatchOperation]):
        """Execute batch update operations"""
        # Updates typically need to be done individually since they have different WHERE clauses
        for op in operations:
            self._execute_single_operation(db, op)
    
    def _batch_upsert(self, db, table: str, operations: List[BatchOperation]):
        """Execute batch upsert operations"""
        data_list = [op.data for op in operations]
        db.client.table(table).upsert(data_list).execute()
    
    def _execute_single_operation(self, db, operation: BatchOperation):
        """Execute a single operation as fallback"""
        if operation.operation_type == 'insert':
            db.client.table(operation.table).insert(operation.data).execute()
        elif operation.operation_type == 'update':
            # Need to extract ID or unique field for update
            if 'session_id' in operation.data:
                db.client.table(operation.table).update(operation.data).eq('session_id', operation.data['session_id']).execute()
            elif 'id' in operation.data:
                db.client.table(operation.table).update(operation.data).eq('id', operation.data['id']).execute()
        elif operation.operation_type == 'upsert':
            db.client.table(operation.table).upsert(operation.data).execute()
    
    def force_flush(self):
        """Force flush all pending operations"""
        with self.lock:
            if self.operations:
                self._schedule_flush()
    
    def shutdown(self):
        """Shutdown the batch processor"""
        self.force_flush()
        self.executor.shutdown(wait=True)

class OptimizedDatabase:
    """Optimized database operations with pooling and batching"""
    
    def __init__(self):
        self.connection_pool = ConnectionPool(max_connections=15)
        self.batch_processor = BatchProcessor(batch_size=25, flush_interval=1.5)
        
        # Warm up connection pool with a few connections
        self._warm_connection_pool()
    
    def _warm_connection_pool(self):
        """Pre-create a few connections to warm the pool"""
        try:
            connections = []
            for i in range(3):  # Create 3 initial connections
                conn = self.connection_pool._create_connection()
                if conn:
                    connections.append(conn)
                    self.connection_pool.total_connections += 1
            
            # Return connections to pool
            for conn in connections:
                self.connection_pool.return_connection(conn)
                
            logger.info(f"Warmed connection pool with {len(connections)} connections")
            
        except Exception as e:
            logger.error(f"Failed to warm connection pool: {e}")
    
    @asynccontextmanager
    async def get_connection(self):
        """Async context manager for database connections"""
        connection = None
        try:
            # Get connection from pool in thread executor
            loop = asyncio.get_event_loop()
            connection = await loop.run_in_executor(None, self.connection_pool.get_connection)
            
            if not connection:
                raise Exception("Failed to get database connection")
            
            yield connection
            
        finally:
            if connection:
                # Return connection to pool in thread executor
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.connection_pool.return_connection, connection)
    
    # Optimized database operations
    
    async def save_tracking_data_optimized(self, session_id: str, tracking_data: Dict[str, Any]):
        """Save tracking data with optimization"""
        operation = BatchOperation(
            operation_type='insert',
            table='tracking_data',
            data={
                'session_id': session_id,
                **tracking_data,
                'created_at': datetime.now().isoformat()
            },
            timestamp=time.time()
        )
        
        # Add to batch processor for efficient processing
        self.batch_processor.add_operation(operation)
    
    async def save_response_batch_optimized(self, session_id: str, responses: List[Dict[str, Any]]):
        """Save multiple responses efficiently"""
        for response_data in responses:
            operation = BatchOperation(
                operation_type='insert',
                table='responses',
                data={
                    'session_id': session_id,
                    **response_data,
                    'created_at': datetime.now().isoformat()
                },
                timestamp=time.time()
            )
            self.batch_processor.add_operation(operation)
    
    async def update_session_optimized(self, session_id: str, session_data: Dict[str, Any]):
        """Update session with optimization"""
        operation = BatchOperation(
            operation_type='upsert',
            table='lead_sessions',
            data={
                'session_id': session_id,
                **session_data,
                'last_updated': datetime.now().isoformat()
            },
            timestamp=time.time()
        )
        
        self.batch_processor.add_operation(operation)
    
    # Read operations with connection pooling
    
    async def get_session_optimized(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data with connection pooling"""
        async with self.get_connection() as conn:
            try:
                start_time = time.time()
                result = conn.client.table('lead_sessions').select('*').eq('session_id', session_id).execute()
                duration = (time.time() - start_time) * 1000
                
                # Log performance
                monitor.log_query(
                    query_hash=f"get_session_{session_id[:8]}",
                    query_type='SELECT',
                    table_name='lead_sessions',
                    duration_ms=duration,
                    success=True,
                    row_count=len(result.data) if result.data else 0
                )
                
                return result.data[0] if result.data else None
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                monitor.log_query(
                    query_hash=f"get_session_{session_id[:8]}",
                    query_type='SELECT',
                    table_name='lead_sessions',
                    duration_ms=duration,
                    success=False,
                    error_message=str(e)
                )
                raise
    
    async def get_responses_optimized(self, session_id: str) -> List[Dict[str, Any]]:
        """Get session responses with connection pooling"""
        async with self.get_connection() as conn:
            try:
                start_time = time.time()
                result = conn.client.table('responses').select('*').eq('session_id', session_id).order('created_at').execute()
                duration = (time.time() - start_time) * 1000
                
                monitor.log_query(
                    query_hash=f"get_responses_{session_id[:8]}",
                    query_type='SELECT',
                    table_name='responses',
                    duration_ms=duration,
                    success=True,
                    row_count=len(result.data) if result.data else 0
                )
                
                return result.data or []
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                monitor.log_query(
                    query_hash=f"get_responses_{session_id[:8]}",
                    query_type='SELECT',
                    table_name='responses',
                    duration_ms=duration,
                    success=False,
                    error_message=str(e)
                )
                raise
    
    async def get_active_forms_optimized(self, days_back: int = 7) -> List[str]:
        """Get list of active forms with optimization"""
        async with self.get_connection() as conn:
            try:
                start_time = time.time()
                
                # Query for forms with recent sessions
                result = conn.client.table('lead_sessions').select('form_id').gte('started_at', 
                    (datetime.now() - datetime.timedelta(days=days_back)).isoformat()
                ).execute()
                
                duration = (time.time() - start_time) * 1000
                
                # Extract unique form IDs
                form_ids = list(set(row['form_id'] for row in result.data if row.get('form_id')))
                
                monitor.log_query(
                    query_hash="get_active_forms",
                    query_type='SELECT',
                    table_name='lead_sessions',
                    duration_ms=duration,
                    success=True,
                    row_count=len(form_ids)
                )
                
                return form_ids
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                monitor.log_query(
                    query_hash="get_active_forms",
                    query_type='SELECT',
                    table_name='lead_sessions',
                    duration_ms=duration,
                    success=False,
                    error_message=str(e)
                )
                raise
    
    # Health and statistics
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get performance optimization statistics"""
        return {
            'connection_pool': self.connection_pool.get_stats(),
            'batch_processor': {
                'pending_operations': len(self.batch_processor.operations),
                'last_flush_seconds_ago': time.time() - self.batch_processor.last_flush
            },
            'database_performance': monitor.get_performance_summary(minutes_back=60)
        }
    
    def force_flush_all(self):
        """Force flush all pending operations"""
        self.batch_processor.force_flush()
    
    def shutdown(self):
        """Shutdown optimized database"""
        self.batch_processor.shutdown()

# Global optimized database instance
optimized_db = OptimizedDatabase()

# Integration with existing async_operations
def integrate_with_async_operations():
    """Integrate optimized database with existing async operations"""
    from .async_operations import AsyncDatabaseOps
    
    # Replace methods in AsyncDatabaseOps to use optimized database
    original_async_db = AsyncDatabaseOps()
    
    def optimized_save_tracking_data(session_id: str, tracking_data: Dict[str, Any]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(optimized_db.save_tracking_data_optimized(session_id, tracking_data))
        finally:
            loop.close()
    
    def optimized_save_response_batch(session_id: str, responses: List[Dict[str, Any]]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(optimized_db.save_response_batch_optimized(session_id, responses))
        finally:
            loop.close()
    
    def optimized_update_session_state(session_id: str, state_data: Dict[str, Any]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(optimized_db.update_session_optimized(session_id, state_data))
        finally:
            loop.close()
    
    # Replace the methods
    original_async_db.save_tracking_data = optimized_save_tracking_data
    original_async_db.save_response_batch = optimized_save_response_batch
    original_async_db.update_session_state = optimized_update_session_state
    
    return original_async_db

# Export main components
__all__ = [
    'OptimizedDatabase',
    'ConnectionPool',
    'BatchProcessor',
    'optimized_db',
    'integrate_with_async_operations'
]