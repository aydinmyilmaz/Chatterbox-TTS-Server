import runpod
from chatterbox_tts import ChatterboxTTS
import torch

# Load model once (on cold start)
print("🚀 Loading multilingual Chatterbox model...")
model = ChatterboxTTS.load_model(repo_id="ResembleAI/chatterbox-multilingual")

def handler(event):
    """
    Serverless handler function.
    RunPod calls this for each incoming job.
    """
    input_data = event.get("input", {})
    text = input_data.get("text", "")
    language = input_data.get("language", "en")

    if not text:
        return {"error": "Missing 'text' input."}

    print(f"🗣️ Generating TTS for '{text}' [{language}]")

    # Generate speech
    output_wav = model.tts(text, language=language)
    output_path = "/tmp/output.wav"
    output_wav.save(output_path)

    return {
        "status": "success",
        "language": language,
        "output": runpod.serverless.utils.upload_output(output_path)
    }

# Required entrypoint
runpod.serverless.start({"handler": handler})
