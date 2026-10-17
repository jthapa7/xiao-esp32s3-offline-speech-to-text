
import time
import wave
import io
import serial
from faster_whisper import WhisperModel

PORT = "COM12"       # Change to your XIAO COM port
BAUD = 115200
SAMPLE_RATE = 16000

print("Loading offline speech model...")
model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8"
)
print("Model ready. No cloud API required.")


def read_exact(ser, size):
    data = bytearray()

    while len(data) < size:
        chunk = ser.read(size - len(data))
        if not chunk:
            raise TimeoutError("Timed out receiving microphone audio")
        data.extend(chunk)

    return bytes(data)


def main():
    with serial.Serial(PORT, BAUD, timeout=30) as ser:
        time.sleep(2)
        ser.reset_input_buffer()

        while True:
            input("\nPress Enter to record 3 seconds of speech...")
            print("Speak now!")

            ser.write(b"REC\n")
            ser.flush()

            # Wait for the ESP32 audio header
            while True:
                line = ser.readline().decode(
                    "ascii", errors="replace"
                ).strip()

                if line.startswith("AUDIO "):
                    audio_size = int(line.split()[1])
                    break

                if line.startswith("ERROR:"):
                    raise RuntimeError(line)

            pcm = read_exact(ser, audio_size)

            # Convert raw PCM into a WAV file in memory
            wav_data = io.BytesIO()

            with wave.open(wav_data, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(SAMPLE_RATE)
                wav.writeframes(pcm)

            wav_data.seek(0)

            # Transcribe locally on the PC
            print("Transcribing locally...")

            segments, info = model.transcribe(
                wav_data,
                language="en",
                beam_size=1,
                vad_filter=False
            )

            transcript = " ".join(
                segment.text.strip() for segment in segments
            ).strip()

            if not transcript:
                transcript = "[No speech detected]"

            print("\nRecognized text:", transcript)

            # Send result back to the ESP32
            transcript = " ".join(transcript.split())
            ser.write(("TEXT:" + transcript + "\n").encode("utf-8"))
            ser.flush()

            # Read the ESP32 acknowledgement
            reply = ser.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            print("ESP32:", reply)


if __name__ == "__main__":
    main()
