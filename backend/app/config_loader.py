import yaml
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigurationLoader:
    """Load and merge YAML configuration files with environment variables"""

    def __init__(self, config_dir: str = None):
        import os
        if config_dir is None:
            # Try different relative paths based on where we're running from
            if os.path.exists("api/config"):
                config_dir = "api/config"  # Running from project root
            elif os.path.exists("config"):
                config_dir = "config"      # Running from api directory
            else:
                config_dir = "../config"   # Running from subdirectory
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, Any] = {}
        load_dotenv(".env.local")

    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load a specific YAML configuration file"""
        config_path = self.config_dir / f"{config_name}.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        self.configs[config_name] = config
        return config

    def load_all_configs(self) -> Dict[str, Any]:
        """Load all YAML configuration files in the config directory"""
        config_files = # TODO

        for config_name in config_files:
            try:
                self.load_config(config_name)
            except FileNotFoundError:
                print(f"Warning: Configuration file {config_name}.yaml not found")

        return self.configs

    def get_config(self, config_name: str) -> Dict[str, Any]:
        """Get a loaded configuration by name"""
        if config_name not in self.configs:
            return self.load_config(config_name)
        return self.configs[config_name]

    def get_env_or_config(self, env_key: str, config_path: str, default: Any = None) -> Any:
        """Get value from environment variable or config file, with fallback to default"""
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value

        try:
            config_parts = config_path.split('.')
            config_name = config_parts[0]
            config = self.get_config(config_name)

            value = config
            for part in config_parts[1:]:
                value = value.get(part, {})

            return value if value != {} else default
        except (KeyError, FileNotFoundError):
            return default


# Global configuration loader instance
config_loader = ConfigurationLoader()
