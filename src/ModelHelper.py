from src.Model import Model


def createModel(name: str, provider: str, api_key: str) -> Model:
    return Model(name=name, provider=provider, api_key=api_key)
