import requests
import base64
import io
import json
from pydub import AudioSegment
from pydub.playback import play

# API call
url = "https://api.sarvam.ai/text-to-speech"
payload = {
    "inputs": ["Hello! app kaise hai, aashsa hai ki moz ho rho hongi "],
    "target_language_code": "hi-IN",
    "speaker": "meera",
    "pitch": 0,
    "pace": 1.65,
    "loudness": 1.5,
    "speech_sample_rate": 8000,
    "enable_preprocessing": True,
    "model": "bulbul:v1",
}
headers = {
    "Content-Type": "application/json",
    'API-Subscription-Key': 'b56d5c2c-a65b-4d2a-a32c-8bfa31f7c6af'
}

response = requests.post(url, json=payload, headers=headers)

# Parse the JSON response
response_data = json.loads(response.text)

# Extract the base64 audio from the 'audios' key
if 'audios' in response_data and len(response_data['audios']) > 0:
    base64_audio = response_data['audios'][0]
else:
    print("No audio data found in response")
    exit(1)

# Remove non-base64 characters (like newlines or spaces, if any)
base64_audio = base64_audio.replace('\n', '').replace('\r', '')

# Ensure base64 padding
missing_padding = len(base64_audio) % 4
if missing_padding != 0:
    base64_audio += '=' * (4 - missing_padding)

# Decode the base64 audio
try:
    audio_data = base64.b64decode(base64_audio)
except base64.binascii.Error as e:
    print("Error decoding base64 audio:", e)
    exit(1)

# Convert to an audio stream
audio_stream = io.BytesIO(audio_data)

# Load the audio into an AudioSegment object (assuming it's in MP3 format)
audio_segment = AudioSegment.from_file(audio_stream, format="mp3")

# Play the audio
play(audio_segment)
