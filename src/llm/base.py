from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        json_output: bool = False,
    ) -> str:
        """
        Generate a response from the language model.

        Args:
            prompt: User prompt.
            system_prompt: Optional system instructions.
            json_output: Whether structured JSON output is expected.

        Returns:
            Model response as a string.
        """
        pass