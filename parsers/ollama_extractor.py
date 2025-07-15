class OllamaExtractor:
    def __init__(self, model):
        self.model = model

    def get_response(self, email_subject, email_body):
        return self.model.get_response(email_subject, email_body)
