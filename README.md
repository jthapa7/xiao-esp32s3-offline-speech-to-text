# XIAO ESP32-S3 Sense — Offline Speech-to-Text

An embedded speech recognition prototype using the onboard PDM microphone of the Seeed Studio XIAO ESP32-S3 Sense and local AI transcription on a Windows PC.

The ESP32 captures audio and transfers raw PCM samples over USB serial. A Python application uses Faster-Whisper to transcribe the audio locally, without sending recordings to a cloud speech recognition service.

## Features

- Onboard PDM microphone input
- 16 kHz, 16-bit, mono audio capture
- USB serial communication between the ESP32 and PC
- Local speech recognition using Faster-Whisper
- No cloud API key required
- Transcript returned to the ESP32 over serial
- Python virtual environment for reproducible setup

## System Architecture

```text
Voice input
    |
    v
XIAO ESP32-S3 Sense
(PDM microphone)
    |
    | USB serial: PCM audio
    v
Python application on Windows
    |
    v
Faster-Whisper
(local inference)
    |
    | Recognized text
    v
Python application
    |
    | USB serial: transcript
    v
XIAO ESP32-S3 Sense
```

## Hardware

- Seeed Studio XIAO ESP32-S3 Sense
- USB data cable
- Windows PC

## Software

- Arduino IDE with ESP32 board support
- Python 3.10 or another Python version supported by the installed dependencies
- Visual Studio Code (recommended)
- Faster-Whisper
- PySerial

## Project Structure

```text
firmware/
  speech/
    speech.ino
python/
  speechToText.py
requirements.txt
.gitignore
README.md
LICENSE
```

## Setup

### 1. Flash the firmware

Open `firmware/speech/speech.ino` in Arduino IDE.

Select the appropriate XIAO ESP32-S3 board and COM port, then upload the sketch.

The firmware uses a 16 kHz mono PDM audio configuration with GPIO 42 as the clock and GPIO 41 as the data pin.

### 2. Create a Python environment

Open a terminal in the repository directory:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure the serial port

Open `python/speechToText.py` and update the `PORT` variable to match the COM port assigned to the XIAO:

```python
PORT = "COM12"
BAUD = 115200
```

The serial port must not be open in Arduino Serial Monitor while Python is running.

### 4. Run speech recognition

From the repository root, execute:

```powershell
.\.venv\Scripts\python.exe .\python\speechToText.py
```

The first run downloads the Faster-Whisper model. An internet connection is needed for this initial download.

Press Enter when prompted and speak during the three-second recording window.

The application prints the recognized text in the terminal and sends it back to the ESP32.

## How It Works

1. Python sends a `REC` command to the ESP32.
2. The ESP32 captures three seconds of microphone audio.
3. The ESP32 sends an audio length header followed by raw PCM bytes.
4. Python converts the PCM audio into a WAV buffer.
5. Faster-Whisper transcribes the recording locally.
6. Python returns the recognized text using the `TEXT:` serial protocol.

## Current Limitations

- Fixed three-second recording window
- English transcription using the `base.en` model
- Requires a PC for speech recognition
- USB serial is used for both audio and text transfer
- No continuous streaming or automatic silence detection yet

## Future Improvements

- Variable-length recording and voice activity detection
- Wake-word detection
- Multilingual speech recognition
- Text display on an external LCD
- Integration with a desk AI companion
- Improved serial protocol and error handling

## Privacy

Audio is processed locally by Faster-Whisper after the model has been downloaded. The application does not require a cloud transcription API.

## License

This project is released under the MIT License. See `LICENSE` for details.