import os
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient

#
# ModelHelper
# This class is used to create model clients for OpenAI, Azure OpenAI and others.
#
class ModelHelper:

    @staticmethod
    def CreateModel(modelName, provider, apikey):
        if provider.lower() == "azure-openai":
            return AzureOpenAIChatCompletionClient(model=modelName, api_key=apikey)
        elif provider.lower() == "openai":
            return OpenAIChatCompletionClient(model=modelName, api_key=apikey)