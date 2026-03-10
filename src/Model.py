from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient


class Model:
    """Represents a model configuration and its underlying provider client."""

    def __init__(self, name: str, provider: str, api_key: str):
        self.name = name
        self.provider = provider
        self.api_key = api_key

        if provider.lower() == "azure-openai":
            self.client = AzureOpenAIChatCompletionClient(model=name, api_key=api_key)
        elif provider.lower() == "openai":
            self.client = OpenAIChatCompletionClient(model=name, api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
    def getModelClient(self):
        return self.client
