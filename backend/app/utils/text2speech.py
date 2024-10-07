import os
import requests
import base64
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

sarvam_txt2speech_api_key = os.getenv('SARVAM_TXT2SPEECH')
url = "https://api.sarvam.ai/text-to-speech"

headers = {
        "Content-Type": "application/json",
        "API-Subscription-Key": sarvam_txt2speech_api_key
    }

def txt2speech(llm_response: str):
    payload = {
        "inputs": [llm_response],
        "target_language_code": "hi-IN",
        "speaker": "meera",
        "pitch": 0,
        "pace": 0.75,
        "loudness": 1.5,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
    audio_base64 = response.text.split("audios\":[\"")[1].split("\"]}")[0]

    audio_data = base64.b64decode(audio_base64)
    audio_path = "output_audio.wav"

    return audio_path, audio_data, audio_base64
