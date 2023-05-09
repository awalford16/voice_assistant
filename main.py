from speech import SpeechToText
from vad import vad
from ai import ChatAI

sm = SpeechToText()
ai = ChatAI()

messages = []

# while(True):
# run audio
audio = vad()
sm.transcribe()

response = ai.get_response(sm.final_transcript)
print(response)