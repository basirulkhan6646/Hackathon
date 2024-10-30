import os
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
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
    #  recording_url = root.find("Call/RecordingUrl").text
    #  return recording_url



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
    # audio_url = "https://recordings.exotel.com/exotelrecordings/insync2/8fb326e4f12d7c217d54d45375b9189r.mp3"
    audio_file_path = download_audio_file(audio_url)
    # audio_file = open(audio_file_path, "rb")
    with open(audio_file_path, "rb") as audio_file:
     transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcription.text


# print (get_order_details_from_audio())
# app2 = FastAPI()

# @app2.get("/openai-speech-to-text")
# async def voice_to_text( ):
#     """
#     Generates a json packet for b2b order details.
#     """
#     try:
#         response = get_order_details_from_audio()   
#         return { "transcribed_text": response}
#     except Exception as e:
#         return {"error": str(e)}


# if __name__ == "__main__":
#     uvicorn.run (app2, host="localhost", port=8001)