"""
Targeted configuration loader for environment-specific settings.
Loads only what's needed from YAML files without global imports.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration for current environment"""
    url: str
    publishable_key: str
    secret_key: str
    pool_size: int
    pool_max_overflow: int
    pool_timeout: int
    pool_recycle: int
    query_timeout: int
    connection_timeout: int
    retry_attempts: int
    retry_delay: int
    health_check_enabled: bool
    health_check_interval: int
    health_check_timeout: int


@dataclass  
class APIConfig:
    """API configuration for current environment"""
    title: str
    version: str
    description: str
    host: str
    port: int
    reload: bool
    workers: int
    cors_origins: list
    cors_methods: list
    cors_headers: list
    cors_credentials: bool
    max_request_size: int
    request_timeout: int
    keep_alive: int


@dataclass
class RateLimitConfig:
    """Rate limiting configuration for current environment"""
    enabled: bool
    requests_per_minute: int
    burst_size: int
    window_seconds: int
    per_ip: bool
    redis_enabled: bool
    include_headers: bool


@dataclass
class SecurityConfig:
    """Security configuration for current environment"""
    max_input_length: int
    max_file_size: int
    sanitize_inputs: bool
    auth_enabled: bool
    jwt_expire_minutes: int
    require_api_key: bool
    admin_key_required: bool
    force_https: bool
    hsts_enabled: bool
    csp_enabled: bool
    session_timeout: int
    max_sessions_per_ip: int


class ConfigLoader:
    """Loads targeted configuration sections based on environment"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = Path(__file__).parent.parent.parent / "config"
        self.config_dir = Path(config_dir)
        self.environment = os.getenv('ENVIRONMENT', 'development').lower()
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a specific YAML file"""
        config_path = self.config_dir / filename
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as file:
            content = file.read()
            
            # Replace environment variables
            for key, value in os.environ.items():
                content = content.replace(f"${{{key}}}", value)
            
            return yaml.safe_load(content)
    
    def _get_env_config(self, config: Dict[str, Any], section: str) -> Dict[str, Any]:
        """Get environment-specific config for a section"""
        base_config = config.get(section, {})
        env_config = base_config.get(self.environment, {})
        
        # Merge base config with environment-specific overrides
        if isinstance(base_config, dict):
            result = {k: v for k, v in base_config.items() if not isinstance(v, dict) or k not in ['development', 'staging', 'production']}
            result.update(env_config)
            return result
        return env_config
    
    def load_database_config(self) -> DatabaseConfig:
        """Load database configuration for current environment"""
        config = self._load_yaml('database.yaml')
        
        # Connection info (same for all environments)
        connection = config.get('connection', {})
        
        # Environment-specific pool settings
        pool_config = self._get_env_config(config, 'pool')
        query_config = self._get_env_config(config, 'query') 
        health_config = self._get_env_config(config, 'health_check')
        
        return DatabaseConfig(
            url=connection.get('url', ''),
            publishable_key=connection.get('publishable_key', ''),
            secret_key=connection.get('secret_key', ''),
            pool_size=pool_config.get('size', 5),
            pool_max_overflow=pool_config.get('max_overflow', 10),
            pool_timeout=pool_config.get('timeout', 30),
            pool_recycle=pool_config.get('recycle', 3600),
            query_timeout=query_config.get('timeout', 30),
            connection_timeout=query_config.get('connection_timeout', 10),
            retry_attempts=query_config.get('retry_attempts', 3),
            retry_delay=query_config.get('retry_delay', 1),
            health_check_enabled=config.get('health_check', {}).get('enabled', True),
            health_check_interval=health_config.get('interval', 300),
            health_check_timeout=health_config.get('timeout', 10)
        )
    
    def load_api_config(self) -> APIConfig:
        """Load API configuration for current environment"""
        config = self._load_yaml('api.yaml')
        
        server_config = self._get_env_config(config, 'server')
        cors_config = self._get_env_config(config, 'cors')
        request_config = self._get_env_config(config, 'request')
        
        # Server settings
        server_base = config.get('server', {})
        
        return APIConfig(
            title=server_base.get('title', 'API'),
            version=server_base.get('version', '1.0.0'),
            description=server_base.get('description', ''),
            host=server_base.get('host', '0.0.0.0'),
            port=server_base.get('port', 8000),
            reload=server_config.get('reload', False),
            workers=server_config.get('workers', 1),
            cors_origins=cors_config.get('origins', []),
            cors_methods=config.get('cors', {}).get('methods', []),
            cors_headers=config.get('cors', {}).get('headers', []),
            cors_credentials=config.get('cors', {}).get('credentials', True),
            max_request_size=request_config.get('max_size', 10485760),
            request_timeout=request_config.get('timeout', 30),
            keep_alive=request_config.get('keep_alive', 5)
        )
    
    def load_rate_limit_config(self) -> RateLimitConfig:
        """Load rate limiting configuration for current environment"""
        config = self._load_yaml('rate_limiting.yaml')
        
        rate_config = self._get_env_config(config, 'rate_limit')
        settings = config.get('settings', {})
        headers = config.get('headers', {})
        
        return RateLimitConfig(
            enabled=rate_config.get('enabled', False),
            requests_per_minute=rate_config.get('requests_per_minute', 60),
            burst_size=rate_config.get('burst_size', 10),
            window_seconds=settings.get('window_seconds', 60),
            per_ip=settings.get('per_ip', True),
            redis_enabled=settings.get('redis_enabled', False),
            include_headers=headers.get('include_headers', True)
        )
    
    def load_security_config(self) -> SecurityConfig:
        """Load security configuration for current environment"""
        config = self._load_yaml('security.yaml')
        
        validation_config = self._get_env_config(config, 'validation')
        auth_config = self._get_env_config(config, 'auth')
        api_security_config = self._get_env_config(config, 'api_security')
        headers_config = self._get_env_config(config, 'headers')
        sessions_config = self._get_env_config(config, 'sessions')
        
        validation_base = config.get('validation', {})
        
        return SecurityConfig(
            max_input_length=validation_config.get('max_input_length', 10000),
            max_file_size=validation_config.get('max_file_size', 5242880),
            sanitize_inputs=validation_base.get('sanitize_inputs', True),
            auth_enabled=auth_config.get('enabled', False),
            jwt_expire_minutes=auth_config.get('jwt_expire_minutes', 60),
            require_api_key=api_security_config.get('require_api_key', False),
            admin_key_required=api_security_config.get('admin_key_required', False),
            force_https=headers_config.get('force_https', False),
            hsts_enabled=headers_config.get('hsts_enabled', False),
            csp_enabled=headers_config.get('csp_enabled', False),
            session_timeout=sessions_config.get('timeout', 3600),
            max_sessions_per_ip=sessions_config.get('max_per_ip', 20)
        )


def get_database_config() -> DatabaseConfig:
    """Get database configuration for current environment"""
    loader = ConfigLoader()
    return loader.load_database_config()


def get_api_config() -> APIConfig:
    """Get API configuration for current environment"""
    loader = ConfigLoader()
    return loader.load_api_config()


def get_rate_limit_config() -> RateLimitConfig:
    """Get rate limiting configuration for current environment"""
    loader = ConfigLoader()
    return loader.load_rate_limit_config()


def get_security_config() -> SecurityConfig:
    """Get security configuration for current environment"""
    loader = ConfigLoader()
    return loader.load_security_config()