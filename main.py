import base64
import azure.cognitiveservices.speech as speechsdk
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder





def get_speech(text, voice):
    output = {}
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
    output['text'] = text
    output['processed_text'] = processed_text
    output['audioMime'] = audioMime
    output['raw_bytes'] = raw_bytes
    return output


app = FastAPI()


class Item(BaseModel):
    text: str
    voice: str


@app.post("/v1")
async def voices(item: Item):
    text = item.text
    voice = item.voice
    Output = get_speech(text, voice)
    Output['raw_bytes'] = jsonable_encoder(Output['raw_bytes'], custom_encoder={
        bytes: lambda v: base64.b64encode(v).decode('utf-8')})
    return Output
