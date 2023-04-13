class RequestBody:
    model = "gpt-3.5-turbo"
    temperature = 0

    def __init__(self, model, temperature, message, max_tokens, **kwargs):
        self.model = model
        self.temperature = temperature
        self.model = model
        self.message = message
        self.max_tokens = max_tokens
        self.kwargs = kwargs
