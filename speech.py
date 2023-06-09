import speechmatics
import ssl
from httpx import HTTPStatusError
import os
from elevenlabs import generate, play

API_KEY = os.environ.get("SM_API_TOKEN")
PATH_TO_FILE = "./recording.wav"
LANGUAGE = "en"
CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"

class SpeechToText:
    def __init__(self):
        self.final_transcript = ""

        ssl_context = ssl.SSLContext()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Create a transcription client
        self.ws = speechmatics.client.WebsocketClient(
            speechmatics.models.ConnectionSettings(
                url=CONNECTION_URL,
                auth_token=API_KEY,
                ssl_context = ssl_context,
                generate_temp_token=True, # Enterprise customers don't need to provide this parameter
            )
        )

        # Register the event handler for partial transcript
        self.ws.add_event_handler(
            event_name=speechmatics.models.ServerMessageType.AddPartialTranscript,
            event_handler=self.print_partial_transcript,
        )

        # Register the event handler for full transcript
        self.ws.add_event_handler(
            event_name=speechmatics.models.ServerMessageType.AddTranscript,
            event_handler=self.update_transcript,
        )

        self.settings = speechmatics.models.AudioSettings()

        # Define transcription parameters
        # Full list of parameters described here: https://speechmatics.github.io/speechmatics-python/models
        self.conf = speechmatics.models.TranscriptionConfig(
            language=LANGUAGE,
            enable_partials=True,
            max_delay=5,
        )

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.final_transcript = ""

    # Define an event handler to print the partial transcript
    def print_partial_transcript(self, msg):
        pass

    # Define an event handler to print the full transcript
    def update_transcript(self, msg):
        self.final_transcript = self.final_transcript + msg['metadata']['transcript']


    def transcribe(self):
        print("Starting transcription (type Ctrl-C to stop):")
        with open(PATH_TO_FILE, 'rb') as fd:
            try:
                self.ws.run_synchronously(fd, self.conf, self.settings)
            except KeyboardInterrupt:
                print("\nTranscription stopped.")
            except HTTPStatusError as e:
                if e.response.status_code == 401:
                    print('Invalid API key - Check your API_KEY at the top of the code!')
                else:
                    raise e

class TextToSpeech:
    def talk(self, msg):
        audio = generate(
            text=msg,
            voice="Bella",
            model="eleven_monolingual_v1"
        )

        play(audio)
    # def __init__(self):
    #     self.audio_file_name = "speech.mp3"
    #     mixer.init()

    # def generate_audio_file(self, msg):
    #     tts = gTTS(text=msg, lang='en')
    #     tts.save(self.audio_file_name)

    # def play_audio(self):
    #     mixer.music.load(self.audio_file_name)
    #     # mixer.music.set_speed(1.5)
    #     mixer.music.play()
    #     while mixer.music.get_busy():  # wait for music to finish playing
    #         time.sleep(1)
