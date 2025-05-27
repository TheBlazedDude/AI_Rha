
import torch
import soundfile as sf
import sounddevice as sd
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datetime import datetime
import os

model_name = "facebook/wav2vec2-base-960h"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

def record_and_transcribe():
    duration = 5
    sample_rate = 16000
    print("Listening for 5 seconds...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    audio_data = recording.flatten()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_path = f"data/audio/{timestamp}.wav"
    sf.write(audio_path, audio_data, sample_rate)

    input_values = processor(audio_data, sampling_rate=sample_rate, return_tensors="pt", padding="longest").input_values
    with torch.no_grad():
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

    with open(audio_path.replace(".wav", ".txt"), "w") as f:
        f.write(transcription.strip())

    print("Heard:", transcription.strip())

if __name__ == "__main__":
    record_and_transcribe()
