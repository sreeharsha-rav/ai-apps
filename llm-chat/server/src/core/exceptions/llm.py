class LLMError(Exception):
    """Base exception for LLM-related errors"""
    pass

class ModelNotFoundError(LLMError):
    """Raised when model_id is not found"""
    pass

class ConfigurationError(LLMError):
    """Raised when configuration is invalid"""
    pass

class ClientInitializationError(LLMError):
    """Raised when client initialization fails"""
    pass

class GenerateCompletionError(LLMError):
    """Raised when generating completion fails"""
    pass