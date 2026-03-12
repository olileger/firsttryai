from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncAzureOpenAI, AsyncOpenAI


class Model:
    """Represents an OpenAI Agent SDK model configuration."""

    def __init__(self, name: str, provider: str, api_key: str):
        self.name = name
        self.provider = provider
        self.api_key = api_key

        normalized_provider = provider.lower()
        if normalized_provider == "azure-openai":
            self._client = AsyncAzureOpenAI(api_key=api_key)
        elif normalized_provider == "openai":
            self._client = AsyncOpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        self._model = OpenAIChatCompletionsModel(
            model=name,
            openai_client=self._client
        )

    def getUnderlyingModel(self):
        return self._model
