# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

class ChatAI:
    def __init__(self):
        pass

    def get_response(self, msg):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": msg}
                ]
        )
        return response['choices'][0]['message']['content']
