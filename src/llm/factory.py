from src.config.settings import settings
from src.llm.gemini import GeminiLLM


def get_llm():
    """
    Returns the configured LLM provider.
    """

    provider = settings.LLM_PROVIDER.lower()

    if provider == "gemini":
        return GeminiLLM()

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )