# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

class ChatAI:
    def __init__(self, messages):
        self.messages = messages

    def get_response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return response['choices'][0]['message']['content']
