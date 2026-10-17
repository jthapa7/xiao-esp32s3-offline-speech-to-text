
#include <ESP_I2S.h>

I2SClass I2S;

const int SAMPLE_RATE = 16000;
const int RECORD_SECONDS = 3;
const int NUM_SAMPLES = SAMPLE_RATE * RECORD_SECONDS;

String lastTranscript = "";


void setup() {
  Serial.begin(115200);
  delay(1000);

  I2S.setPinsPdmRx(42, 41);

  if (!I2S.begin(
        I2S_MODE_PDM_RX,
        SAMPLE_RATE,
        I2S_DATA_BIT_WIDTH_16BIT,
        I2S_SLOT_MODE_MONO)) {
    Serial.println("ERROR: Microphone initialization failed");
    while (true) delay(1000);
  }
  Serial.setTimeout(120000);

  Serial.println("READY");
}

void loop() {

  if (!Serial.available()) {
    delay(5);
    return;
  }

  String command = Serial.readStringUntil('\n');
  command.trim();

  if (command == "REC") {
    int16_t *audio = (int16_t *)malloc(NUM_SAMPLES * sizeof(int16_t));

    if (!audio) {
      Serial.println("ERROR: Out of memory");
      return;
    }

    // Capture 3 seconds of mono PCM audio.
    for (int i = 0; i < NUM_SAMPLES; i++) {
      int sample = I2S.read();
      audio[i] = (int16_t)sample;
    }

    // Header is ASCII; audio following it is binary PCM.
    Serial.printf("AUDIO %d\n",
                  NUM_SAMPLES * sizeof(int16_t));
    Serial.write((uint8_t *)audio,
                 NUM_SAMPLES * sizeof(int16_t));
    Serial.flush();

    free(audio);

    // Wait for Python to return the transcript.
    String response = Serial.readStringUntil('\n');
    response.trim();

    if (response.startsWith("TEXT:")) {
      lastTranscript = response.substring(5);
      Serial.println("TRANSCRIPT_RECEIVED");
    } else {
      lastTranscript = "No transcript received";
      Serial.println("ERROR: Invalid response");
    }
  }
}
