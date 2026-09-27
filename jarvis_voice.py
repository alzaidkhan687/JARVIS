import asyncio
import os
import queue

import numpy as np
import sounddevice as sd
from google import genai
from google.genai import types

# Gemini Live audio settings — same basic architecture as the main JARVIS project.
MODEL = "models/gemini-3.1-flash-live-preview"
INPUT_RATE = 16000
OUTPUT_RATE = 24000
CHANNELS = 1
BLOCK_SIZE = 1024

mic_queue = queue.Queue()


def mic_callback(indata, frames, time_info, status):
    if status:
        print(f"[MIC] {status}")
    mic_queue.put(indata.copy())


async def send_microphone(session):
    while True:
        data = await asyncio.to_thread(mic_queue.get)
        await session.send_realtime_input(
            audio=types.Blob(
                data=data.astype(np.int16).tobytes(),
                mime_type="audio/pcm",
            )
        )


async def receive_voice(session):
    audio_chunks = []

    async for response in session.receive():
        if response.data:
            audio_chunks.append(response.data)

        if response.server_content and response.server_content.turn_complete:
            if audio_chunks:
                audio = b"".join(audio_chunks)
                samples = np.frombuffer(audio, dtype=np.int16)

                # Play Gemini's generated voice response.
                sd.play(samples, OUTPUT_RATE)
                await asyncio.to_thread(sd.wait)
                audio_chunks.clear()

            print("[JARVIS] Turn complete")


async def main():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "See README.md for setup instructions."
        )

    client = genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1beta"},
    )

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        input_audio_transcription={},
        output_audio_transcription={},
        system_instruction=(
            "You are JARVIS, a helpful AI voice assistant. "
            "Keep replies short, natural and conversational. "
            "Speak clearly and directly."
        ),
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Puck"
                )
            )
        ),
    )

    print("JARVIS is starting...")
    print("Speak into your microphone. Press Ctrl+C to stop.")

    with sd.InputStream(
        samplerate=INPUT_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=BLOCK_SIZE,
        callback=mic_callback,
    ):
        async with client.aio.live.connect(
            model=MODEL,
            config=config,
        ) as session:
            print("[JARVIS] Connected. Listening...")

            await asyncio.gather(
                send_microphone(session),
                receive_voice(session),
            )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[JARVIS] Stopped.")
