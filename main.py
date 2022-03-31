import base64
import azure.cognitiveservices.speech as speechsdk
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder



def get_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription="b11d9472cc9d4f56a5522a6ef450b7f4", region="eastus")
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = synthesizer.speak_text_async(text).get()
    stream = speechsdk.AudioDataStream(result)
    # stream.save_to_wav_file("bg1.mp3")
    audio_buffer = bytes(32000)
    x = stream.read_data(audio_buffer=audio_buffer)
    return audio_buffer


app = FastAPI()


class Item(BaseModel):
    text: str


@app.get("/v1/voice")
async def voices(item: Item):
    text = item.text
    Output = get_speech(text)
    json_compatible_item_data = jsonable_encoder(Output, custom_encoder={
        bytes: lambda v: base64.b64encode(v).decode('utf-8')})
    return json_compatible_item_data
