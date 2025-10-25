import runpod
from runpod.serverless.utils import upload_output
from chatterbox_tts import ChatterboxTTS
import torch
import os

# Load model once on cold start
print("🚀 Loading multilingual Chatterbox model...")
model = ChatterboxTTS.load_model(repo_id="ResembleAI/chatterbox-multilingual")

def handler(event):
    """
    RunPod serverless handler.
    Takes JSON input: {"text": "...", "language": "en"}
    Returns link to generated WAV file.
    """
    try:
        input_data = event.get("input", {})
        text = input_data.get("text", "")
        language = input_data.get("language", "en")

        if not text:
            return {"error": "Missing 'text' field in input."}

        print(f"🗣️ Generating TTS for: '{text}' [{language}]")

        # Generate TTS
        output_audio = model.tts(text, language=language)
        output_path = "/tmp/output.wav"
        output_audio.save(output_path)

        print("✅ Audio generation complete.")
        output_url = upload_output(output_path)

        return {
            "status": "success",
            "language": language,
            "text": text,
            "output_url": output_url
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

# Required RunPod entrypoint
runpod.serverless.start({"handler": handler})
