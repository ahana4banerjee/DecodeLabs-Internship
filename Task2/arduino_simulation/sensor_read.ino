// Define Pins
const int tmpPin = A0;      // TMP36 Temperature Sensor
const int lightPin = A1;    // Photoresistor (LDR) measuring Ambient Light
const int pirPin = 2;       // PIR Motion Sensor

// Variables for timing
unsigned long previousMillis = 0;
const long interval = 5000; // Sample every 5 seconds

void setup() {
  Serial.begin(9600);
  pinMode(pirPin, INPUT);
}

void loop() {
  unsigned long currentMillis = millis();

  // Non-blocking timer execution
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // 1. Read and Calculate Temperature from TMP36
    int tmpReading = analogRead(tmpPin);
    float voltage = tmpReading * (5.0 / 1023.0);
    float temperature = (voltage - 0.5) * 100.0; // Conversion to Celsius

    // 2. Read and Map Ambient Light Level
    int lightReading = analogRead(lightPin);
    // Map the expected analog sensor range to a 0-100% intensity scale
    // Note: In Tinkercad, LDR values vary depending on the lux level applied
    float lightIntensity = map(lightReading, 0, 1023, 0, 100);

    // 3. Read Motion State
    int motion = digitalRead(pirPin);

    // Print to Serial in CSV format: Temperature,Light,Motion
    Serial.print(temperature);
    Serial.print(",");
    Serial.print(lightIntensity);
    Serial.print(",");
    Serial.println(motion);
  }
}