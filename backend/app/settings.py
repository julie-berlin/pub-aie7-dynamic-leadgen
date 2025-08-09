import os
from typing import List
from .config_loader import config_loader


class AppSettings:
    """Application settings loaded from YAML config and environment variables"""

    def __init__(self):
        self._load_settings()

    def _load_settings(self):
        config_loader.load_all_configs()

        # API Settings
        app_config = config_loader.get_config("application")
        self.api_title = app_config["api"]["title"]
        self.api_version = app_config["api"]["version"]
        self.api_description = app_config["api"]["description"]
        self.host = app_config["api"]["host"]
        self.port = app_config["api"]["port"]
        self.reload = app_config["api"]["reload"]

        # Security
        self.cors_origins = app_config["security"]["cors_origins"]

        # Environment
        self.environment = app_config["environment"]["name"]
        self.debug = app_config["environment"]["debug"]
        self.log_level = app_config["environment"]["log_level"]

        # AI Settings
        ai_config = config_loader.get_config("ai_models")
        self.openai_model = ai_config["openai"]["slim_model"]
        self.planning_model = ai_config["openai"]["thinking_model"]
        self.embedding_model = ai_config["openai"]["embedding_model"]
        self.temperature = ai_config["openai"]["temperature"]
        self.max_tokens = ai_config["openai"]["max_tokens"]

        # Environment variables (required)
        self.openai_api_key = config_loader.get_env_or_config("OPENAI_API_KEY", "")
        self.tavily_api_key = config_loader.get_env_or_config("TAVILY_API_KEY", "")
        self.langchain_api_key = config_loader.get_env_or_config("LANGCHAIN_API_KEY", "")
        self.cohere_api_key = config_loader.get_env_or_config("COHERE_API_KEY", "")

        # LangSmith
        self.langchain_tracing = ai_config["langchain"]["tracing_enabled"]
        self.langchain_project = ai_config["langchain"]["project_name"]

        # Vector Database
        vector_config = config_loader.get_config("vector_database")
        self.qdrant_url = os.getenv("QDRANT_URL", vector_config["qdrant"]["url"])
        self.collections = vector_config["qdrant"]["collections"]
        self.collection_name = self.collections["character_chunks"]  # Default for backward compatibility
        self.semantic_collection_name = self.collections["semantic_chunks"]
        self.embedding_dimension = vector_config["qdrant"]["embedding_dimension"]
        self.retrieval_top_k = vector_config["retrieval"]["top_k"]
        self.retrieval_strategy = vector_config["retrieval"]["strategy"]

        # Data Processing
        data_config = config_loader.get_config("data_processing")
        self.data_directory = data_config["documents"]["data_directory"]
        self.chunk_size = data_config["text_splitting"]["chunk_size"]
        self.chunk_overlap = data_config["text_splitting"]["chunk_overlap"]

        # Semantic Splitting
        self.semantic_buffer_size = data_config["semantic_splitting"]["buffer_size"]
        self.semantic_breakpoint_threshold = data_config["semantic_splitting"]["breakpoint_percentile_threshold"]

        # Chunking Strategy
        self.default_chunking_strategy = data_config["chunking"]["default_strategy"]
        self.generate_both_collections = data_config["chunking"]["generate_both_collections"]

        # Evaluation
        self.test_dataset_path = data_config["evaluation"]["test_dataset_path"]

        # Agentic Workflow
        workflow_config = config_loader.get_config("agentic_workflow")
        self.parallel_search_enabled = workflow_config["parallel_search"]["enabled"]
        self.concurrent_searches = workflow_config["parallel_search"]["concurrent_searches"]
        self.planning_timeout = workflow_config["planning_agent"]["timeout_seconds"]

        # Golden Dataset Generation
        golden_config = config_loader.get_config("golden_dataset")
        self.ragas_testset_size = golden_config["ragas"]["testset_size"]
        self.ragas_document_subset_size = golden_config["ragas"]["document_subset_size"]
        self.ragas_generator_model = golden_config["ragas"]["generator_model"]
        self.ragas_generator_temperature = golden_config["ragas"]["generator_temperature"]
        self.ragas_embedding_model = golden_config["ragas"]["embedding_model"]

        self.dataset_output_directory = golden_config["dataset"]["output_directory"]
        self.dataset_filename_prefix = golden_config["dataset"]["filename_prefix"]
        self.dataset_include_timestamp = golden_config["dataset"]["include_timestamp"]

        self.ground_truth_model = golden_config["ground_truth"]["assessment_model"]
        self.ground_truth_temperature = golden_config["ground_truth"]["assessment_temperature"]
        self.ground_truth_max_tokens = golden_config["ground_truth"]["max_tokens"]
        self.ground_truth_rate_limit_delay = golden_config["ground_truth"]["rate_limit_delay"]

        self.user_contexts = golden_config["user_contexts"]
        self.quality_settings = golden_config["quality"]


# Global settings instance
settings = AppSettings()
