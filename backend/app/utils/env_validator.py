"""
Environment variable validation for different deployment environments
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EnvironmentVariable:
    """Definition of an environment variable requirement"""
    name: str
    required: bool = True
    default: Optional[Any] = None
    description: str = ""
    env_specific: Dict[str, bool] = None  # Per-environment requirements
    validator: Optional[callable] = None


class EnvironmentValidator:
    """Validates environment variables based on deployment environment"""
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv('ENVIRONMENT', 'development').lower()
        self.validation_errors: List[str] = []
        self.warnings: List[str] = []
    
    def _validate_url(self, value: str) -> bool:
        """Validate URL format"""
        if not value:
            return False
        return value.startswith(('http://', 'https://'))
    
    def _validate_api_key(self, value: str) -> bool:
        """Validate API key format"""
        if not value:
            return False
        return len(value) > 10  # Basic length check
    
    def _validate_positive_int(self, value: str) -> bool:
        """Validate positive integer"""
        try:
            return int(value) > 0
        except (ValueError, TypeError):
            return False
    
    def _validate_log_level(self, value: str) -> bool:
        """Validate log level"""
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        return value.upper() in valid_levels
    
    def get_required_variables(self) -> List[EnvironmentVariable]:
        """Get list of required environment variables based on environment"""
        base_vars = [
            # Database variables (always required)
            EnvironmentVariable(
                name="SUPABASE_URL",
                required=True,
                description="Supabase project URL",
                validator=self._validate_url
            ),
            EnvironmentVariable(
                name="SUPABASE_PUBLISHABLE_KEY", 
                required=True,
                description="Supabase publishable key",
                validator=self._validate_api_key
            ),
            EnvironmentVariable(
                name="SUPABASE_SECRET_KEY",
                required=True, 
                description="Supabase secret key",
                validator=self._validate_api_key
            ),
            
            # LLM variables
            EnvironmentVariable(
                name="OPENAI_API_KEY",
                required=True,
                description="OpenAI API key for LLM operations",
                validator=self._validate_api_key
            ),
            
            # Optional but recommended variables
            EnvironmentVariable(
                name="LANGCHAIN_API_KEY",
                required=False,
                description="LangChain API key for tracing (optional)",
                validator=self._validate_api_key
            ),
            EnvironmentVariable(
                name="TAVILY_API_KEY",
                required=False,
                description="Tavily API key for search (optional)", 
                validator=self._validate_api_key
            ),
            
            # Environment configuration
            EnvironmentVariable(
                name="ENVIRONMENT",
                required=False,
                default="development",
                description="Deployment environment (development/staging/production)"
            ),
            EnvironmentVariable(
                name="LOG_LEVEL",
                required=False,
                default="INFO",
                description="Logging level",
                validator=self._validate_log_level
            ),
        ]
        
        # Environment-specific variables
        env_specific_vars = []
        
        if self.environment in ['staging', 'production']:
            env_specific_vars.extend([
                EnvironmentVariable(
                    name="ADMIN_API_KEY",
                    required=True,
                    description="Admin API key for protected endpoints",
                    validator=self._validate_api_key
                ),
                EnvironmentVariable(
                    name="JWT_SECRET",
                    required=True,
                    description="JWT secret for authentication",
                    validator=lambda x: len(x) >= 32 if x else False
                ),
            ])
        
        if self.environment == 'production':
            env_specific_vars.extend([
                EnvironmentVariable(
                    name="SENTRY_DSN",
                    required=False,
                    description="Sentry DSN for error tracking",
                    validator=self._validate_url
                ),
                EnvironmentVariable(
                    name="LOG_FILE",
                    required=False,
                    description="Log file path for production logging"
                ),
            ])
        
        return base_vars + env_specific_vars
    
    def validate_environment(self) -> bool:
        """Validate all required environment variables"""
        self.validation_errors = []
        self.warnings = []
        
        required_vars = self.get_required_variables()
        
        logger.info(f"Validating environment variables for {self.environment} environment")
        
        for var in required_vars:
            value = os.getenv(var.name)
            
            # Check if variable is required
            env_required = var.required
            if var.env_specific and self.environment in var.env_specific:
                env_required = var.env_specific[self.environment]
            
            if not value:
                if env_required:
                    self.validation_errors.append(
                        f"Missing required environment variable: {var.name}"
                        f" - {var.description}"
                    )
                elif var.default is not None:
                    os.environ[var.name] = str(var.default)
                    self.warnings.append(
                        f"Using default value for {var.name}: {var.default}"
                    )
                else:
                    self.warnings.append(
                        f"Optional environment variable not set: {var.name}"
                        f" - {var.description}"
                    )
                continue
            
            # Validate format if validator is provided
            if var.validator and not var.validator(value):
                self.validation_errors.append(
                    f"Invalid format for environment variable {var.name}: {value}"
                    f" - {var.description}"
                )
        
        # Log results
        if self.validation_errors:
            logger.error(f"Environment validation failed with {len(self.validation_errors)} errors")
            for error in self.validation_errors:
                logger.error(f"  ❌ {error}")
        
        if self.warnings:
            logger.info(f"Environment validation completed with {len(self.warnings)} warnings")
            for warning in self.warnings:
                logger.warning(f"  ⚠️  {warning}")
        
        if not self.validation_errors and not self.warnings:
            logger.info("✅ All environment variables validated successfully")
        
        return len(self.validation_errors) == 0
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary for reporting"""
        return {
            'environment': self.environment,
            'valid': len(self.validation_errors) == 0,
            'errors': self.validation_errors,
            'warnings': self.warnings,
            'total_variables_checked': len(self.get_required_variables())
        }


def validate_environment(environment: str = None) -> bool:
    """Validate environment variables and return success status"""
    validator = EnvironmentValidator(environment)
    return validator.validate_environment()


def get_validation_summary(environment: str = None) -> Dict[str, Any]:
    """Get environment validation summary"""
    validator = EnvironmentValidator(environment)
    validator.validate_environment()
    return validator.get_validation_summary()


def print_environment_help():
    """Print help for environment variable setup"""
    validator = EnvironmentValidator()
    required_vars = validator.get_required_variables()
    
    print("\n🔧 Environment Variable Setup Help")
    print("=" * 50)
    print(f"Environment: {validator.environment}")
    print("\nRequired variables:")
    
    for var in required_vars:
        if var.required or (var.env_specific and validator.environment in var.env_specific):
            status = "✅ SET" if os.getenv(var.name) else "❌ MISSING"
            print(f"  {status} {var.name}")
            print(f"      {var.description}")
            if var.default:
                print(f"      Default: {var.default}")
    
    print("\nOptional variables:")
    for var in required_vars:
        if not var.required and not (var.env_specific and validator.environment in var.env_specific):
            status = "✅ SET" if os.getenv(var.name) else "⚪ OPTIONAL"
            print(f"  {status} {var.name}")
            print(f"      {var.description}")
    
    print(f"\n💡 Create a .env file in your project root with these variables")
    print(f"💡 Set ENVIRONMENT={validator.environment} to match your deployment")


if __name__ == "__main__":
    # CLI usage for environment validation
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print_environment_help()
    else:
        environment = sys.argv[1] if len(sys.argv) > 1 else None
        success = validate_environment(environment)
        sys.exit(0 if success else 1)