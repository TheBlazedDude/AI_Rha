
import speech_recognition as sr
import os
from datetime import datetime

def listen_and_log():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        audio = r.listen(source, timeout=5)
        try:
            text = r.recognize_google(audio)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f"data/audio/{timestamp}.txt", "w") as f:
                f.write(text)
            print("Heard:", text)
        except sr.UnknownValueError:
            print("Could not understand")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    listen_and_log()
