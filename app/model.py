from transformers import pipeline

class ChatModel:
    def __init__(self, model_name="gpt2"):
        self.generator = pipeline("text-generation", model=model_name)

    def generate_response(self, context, query):
        input_text = f"{context}\n\nUser: {query}\n\nBot:"
        response = self.generator(input_text, max_length=150, num_return_sequences=1)
        return response[0]['generated_text'].split("Bot:")[-1].strip()
