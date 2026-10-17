# XIAO ESP32-S3 Sense — Offline Speech-to-Text

A speech-to-text prototype using the Seeed Studio XIAO ESP32-S3 Sense and a Python application running locally on a computer.

## Features

- Audio capture using the onboard PDM microphone
- USB serial communication between the ESP32-S3 and computer
- Local speech recognition using Faster-Whisper
- English transcription using the `base.en` model
- Transcript returned to the ESP32-S3

## Hardware

- Seeed Studio XIAO ESP32-S3 Sense
- Windows PC connected over USB

## Software

- Arduino IDE with ESP32 board support
- Python 3
- Faster-Whisper
- PySerial

## Project Structure

```text
xiao-esp32s3-offline-speech-to-text/
├── firmware/
├── python/
├── requirements.txt
└── README.md
```

## Setup

Install the Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Open `python/speechToText.py` and update the serial port to match your ESP32-S3, for example `COM12`.

Close Arduino Serial Monitor before starting the Python application.

Run the application from the project root:

```powershell
python .\python\speechToText.py
```

Upload the Arduino sketch from the `firmware` folder to your XIAO ESP32-S3 Sense using Arduino IDE.

## How It Works

1. Python sends a recording command to the ESP32-S3 over USB serial.
2. The ESP32-S3 captures audio from its onboard microphone.
3. The captured audio is sent to the computer.
4. Faster-Whisper transcribes the audio locally.
5. Python sends the recognized text back to the ESP32-S3.

## Privacy

Speech recognition runs locally on the computer using Faster-Whisper. This project does not require a cloud transcription API.

## Future Improvements

- Configurable recording duration
- Improved error handling
- Push-button recording
- Displaying recognized text on the device

## License

License information will be added when a license is selected.
