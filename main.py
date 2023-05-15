from speech import SpeechToText, TextToSpeech
from vad import VAD
from ai import ChatAI
import signal
from sys import exit

kill = False
def exit_gracefully():
  global kill
  print("quitting...")
  kill = True

messages = []
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

sm = SpeechToText()
ai = ChatAI(messages)

while not kill:
    # run audio
    with VAD() as vad:
        audio = vad.vad()

    with SpeechToText() as sm:
        sm.transcribe()
        ai.messages.append({"role":"user", "content":sm.final_transcript})

    response = ai.get_response()
    ai.messages.append({"role":"assistant", "content":response})

    tts = TextToSpeech()

    tts.generate_audio_file(response)
    tts.play_audio()

    if kill:
        exit(0)
