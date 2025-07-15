# parsers/__init__.py
"""
Email parsing module for job application tracking.
"""

from .openai_extractor import OpenAIExtractor
from .ollama_extractor import OllamaExtractor

__all__ = ['OpenAIExtractor', 'OllamaExtractor']
