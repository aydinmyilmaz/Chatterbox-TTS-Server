import runpod
from runpod.serverless.utils import upload_output
from chatterbox_tts import ChatterboxTTS
import torch

# Lazy model initialization
model = None

def get_model():
    global model
    if model is None:
        print("🚀 Loading multilingual Chatterbox model...")
        model = ChatterboxTTS.load_model(repo_id="ResembleAI/chatterbox-multilingual")
    return model

def handler(event):
    """RunPod Serverless handler"""
    input_data = event.get("input", {})
    text = input_data.get("text", "")
    language = input_data.get("language", "en")

    if not text:
        return {"error": "Missing 'text' input."}

    print(f"🗣️ Generating TTS for '{text}' [{language}]")
    model_instance = get_model()

    try:
        output_wav = model_instance.tts(text, language=language)
        output_path = "/tmp/output.wav"
        output_wav.save(output_path)
        return {
            "status": "success",
            "language": language,
            "output_url": upload_output(output_path)
        }
    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})
