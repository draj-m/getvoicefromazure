import base64
import azure.cognitiveservices.speech as speechsdk
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder




def get_speech(text, voice):
    if voice == 'en-GB-LibbyNeural':
        speech_config = speechsdk.SpeechConfig(subscription="b11d9472cc9d4f56a5522a6ef450b7f4", region="eastus")
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        processed_text = text
        audioMime = 'audio/mp3'
        result = synthesizer.speak_text_async(text).get()
        stream = speechsdk.AudioDataStream(result)
        # stream.save_to_wav_file("bg1.mp3")
        raw_bytes = []
        x = 1
        y = bytes
        while x != 0:
            audio_buffer = bytes(1000000)
            x = stream.read_data(audio_buffer=audio_buffer)
            raw_bytes.append(audio_buffer)
            #y = y + audio_buffer
        return text, processed_text, audioMime, raw_bytes


app = FastAPI()


class Item(BaseModel):
    text: str
    voice: str


@app.post("/v1/voice")
async def voices(item: Item):
    text = item.text
    voice = item.voice
    Output = get_speech(text, voice)
    json_compatible_item_data = jsonable_encoder(Output, custom_encoder={
        bytes: lambda v: base64.b64encode(v).decode('utf-8')})
    return json_compatible_item_data
