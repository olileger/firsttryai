import os
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient


def createModel(modelName, provider, apikey):
    """
    Create a model client based on the provider.
    """
    if provider.lower() == "azure-openai":
        return AzureOpenAIChatCompletionClient(model=modelName, api_key=apikey)
    elif provider.lower() == "openai":
        return OpenAIChatCompletionClient(model=modelName, api_key=apikey)