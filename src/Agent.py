class Agent:
    """Provide abstraction for an Agent for an easy library switching."""
    
    def __init__(self, name: str, instruction: str, model: str):
        self.name = name
        self.instruction = instruction
        self.model = model
        # TODO: create the underlying agent on OpenAI SDK and move the property reading to the underlying agent.
    
    @property
    def name(self) -> str:
        return self.name
    
    @property
    def instruction(self) -> str:
        return self.instruction
    
    @property
    def model(self) -> str:
        return self.model
