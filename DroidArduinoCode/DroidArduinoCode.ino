#include <Servo.h>

#define SWITCH_IN 6
#define THROTTLE_IN 7
#define STEERING_IN 8
#define THROTTLE_OUT 9
#define STEERING_OUT 10
#define LED_PIN 13
#define THROTTLE_COMMAND 'T'
#define STEERING_COMMAND 'S'

Servo throttle;
Servo steering;
uint32_t throttlePulse;
uint32_t steeringPulse;
uint8_t command, len;
uint32_t pulse;
uint8_t piControl = 0;

void setup() {
  Serial.begin(115200);
  pinMode(THROTTLE_IN, INPUT);
  pinMode(STEERING_IN, INPUT);
  pinMode(SWITCH_IN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  throttle.attach(THROTTLE_OUT);
  steering.attach(STEERING_OUT);
}

void loop() {
  if (pulseIn(SWITCH_IN, HIGH, 20000) > 1500) {
    piControl = 1;
  } else {
    piControl = 0;
  }
  
  if (Serial.available()) {
    /*
     * Commands from RPi should look like (where each <...> is one byte): 
     * <Servo to control T/S> <number of digits to read n> <digit 1> ... <digit n>
     * e.g. to set steering servo to a pulse width of 1500us: S41500
     * e.g. to set throttle servo to a pulse width of 750us: T3750
     */
    command = Serial.read();

    if (piControl) {
      len = Serial.read() - '0';
      
      pulse = 0;
      for (int i=0; i<len; ++i) {
        pulse *= 10;
        pulse += (Serial.read() - '0');
      }
      
      if (command == THROTTLE_COMMAND) {
        throttle.writeMicroseconds(pulse);
      } else if (command == STEERING_COMMAND) {
        steering.writeMicroseconds(pulse);
      }
    }
  }

  if (!piControl) {
    throttlePulse = pulseIn(THROTTLE_IN, HIGH, 20000);
    throttle.writeMicroseconds(throttlePulse);
  
    steeringPulse = pulseIn(STEERING_IN, HIGH, 20000);
    steering.writeMicroseconds(steeringPulse);
  }
}

