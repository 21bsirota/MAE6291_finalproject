// Utilizing the Linked List Class by ivanseidel
// https://github.com/ivanseidel/LinkedList
#include <LinkedList.h>

const int threshold = 550;
const int avg_samples = 10;

int signal, previous, sum;
unsigned long cur_time, prev_time, interval;
double bpm;

LinkedList<unsigned long> list = LinkedList<unsigned long>();

void setup() {
    // put your setup code here, to run once:
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(115200);

    cur_time = 1;
    prev_time = 0;
    sum = 0;
    for (int i = 0; i < avg_samples; i++) {
        list.add(0);
    }
}

void loop() {
    // put your main code here, to run repeatedly:
    previous = signal;
    signal = analogRead(0);
    // Serial.println("Signal " + String(signal));

    if (signal >= threshold && previous < threshold) {
        // Serial.println("Beat " + String(millis()));

        prev_time = cur_time;
        cur_time = millis();

        interval = cur_time - prev_time;

        sum -= list.pop();
        sum += interval;
        list.unshift(interval);

        bpm = (1.0 / (sum / avg_samples)) * 60000;
        Serial.println("BPM " + String(bpm));
    }

    if (signal > threshold) {
        digitalWrite(LED_BUILTIN, HIGH);
    } else {
        digitalWrite(LED_BUILTIN, LOW);
    }

    delay(20);

}
