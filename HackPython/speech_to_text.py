import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET 

load_dotenv()


def exotel_audio_url():
     exotel_api_key = os.getenv("EXOTEL_API_KEY")
     response = requests.get(exotel_api_key)
     root = ET.fromstring(response.content)
     
     for call_element in root.findall("Call"):
         recording_url = call_element.find("RecordingUrl").text
         if recording_url: 
             return recording_url;

     return None



def download_audio_file(url):
    response = requests.get(url)
    if response.status_code ==200  :
        audio_path = "temp_audio.mp3"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)
        
        return audio_path



def get_order_details_from_audio():

    client = OpenAI (api_key= os.getenv("OPENAI_API_KEY"))
    audio_url = exotel_audio_url()
    audio_file_path = download_audio_file(audio_url)
    with open(audio_file_path, "rb") as audio_file:
     transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcription.text
