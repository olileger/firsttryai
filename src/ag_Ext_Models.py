import os
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient

#
# ModelHelper
# This class is used to create model clients for OpenAI, Azure OpenAI and others.
#
class ModelHelper:

    def CreateModel(modelName, apikeyEnvVarName):
        modelName = ModelHelper._GetModelFullname(modelName)
        if apikeyEnvVarName.startswith("AOAI_"):
            return AzureOpenAIChatCompletionClient(model=modelName, api_key=os.getenv(apikeyEnvVarName))
        elif apikeyEnvVarName.startswith("OAI_"):
            return OpenAIChatCompletionClient(model=modelName, api_key=os.getenv(apikeyEnvVarName))
    
    
    def _GetModelFullname(model):
         match model:
            case "4o":
                return "gpt-4o-2024-08-06"
            case "35t16":
                return "gpt-3.5-turbo-16k"
            case "35t32":
                return "gpt-3.5-turbo-32k"
            case _:
                return model