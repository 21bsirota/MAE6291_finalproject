const int threshold = 700;

int signal, previous;
unsigned long cur_time, prev_time, interval;
double bpm;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(115200);

    cur_time = 1;
    prev_time = 0;
}

void loop() {
    previous = signal;
    signal = analogRead(0);

    if (signal >= threshold && previous < threshold) {
        prev_time = cur_time;
        cur_time = millis();

        interval = cur_time - prev_time;
        bpm = (1.0 / interval) * 60000;
        Serial.println("INT " + String(bpm));
    }

    if (signal > threshold) {
        digitalWrite(LED_BUILTIN, HIGH);
    } else {
        digitalWrite(LED_BUILTIN, LOW);
    }

    delay(20);
}
