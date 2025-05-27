
# Full Baby AI Multimodal Project

Includes:
- Self-learning chat brain with dream mode and reflection
- Persistent `responses.json` with scoring and feedback
- Live camera support
- Voice input (SpeechRecognition or Whisper)
- Vision (OpenCV + CLIP)
- Audio transcription (Whisper)
- Vision/audio memory linking for questions like "What did you see?"

Modules:
- `main_gui.py` (GUI interface)
- `modules/vision_clip.py`
- `modules/audio_whisper.py`
- `modules/chat_memory.py`

To use:
- Run GUI normally: `python gui/main_gui.py`
- Use vision/audio tools by running modules directly or integrating

Next:
- Replace CLIP/Whisper with fully open-source HuggingFace versions (optional)
