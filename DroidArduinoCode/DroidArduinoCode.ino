#include <Servo.h>

#define SWITCH_IN 6
#define THROTTLE_IN 7
#define STEERING_IN 8
#define THROTTLE_OUT 9
#define STEERING_OUT 10
#define LED_PIN 13
#define THROTTLE_COMMAND 'T'
#define STEERING_COMMAND 'S'
#define NUM_READINGS 10

Servo throttle;
Servo steering;
unsigned long throttlePulse;
unsigned long steeringPulse;
unsigned long pulse;
unsigned char command, len;
char piControl = 1;
unsigned int index;
unsigned long t_total, t_average, s_total, s_average;
unsigned int s_readings[NUM_READINGS];
unsigned int t_readings[NUM_READINGS];

void setup() {
  Serial.begin(9600);
  pinMode(THROTTLE_IN, INPUT);
  pinMode(STEERING_IN, INPUT);
  pinMode(SWITCH_IN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  throttle.attach(THROTTLE_OUT);
  steering.attach(STEERING_OUT);
  index = 0;
  s_total = 0;
  s_average = 0;
  t_total = 0;
  t_average = 0;
  for (int i=0; i<NUM_READINGS; ++i) {
    s_readings[i] = 0;
    t_readings[i] = 0;
  }
  throttle.writeMicroseconds(1500);
  steering.writeMicroseconds(1500);
}

void loop() {
  // if controller switch is on, pi has control
  if (pulseIn(SWITCH_IN, HIGH, 40000) > 1500) {
    piControl = 1;
    digitalWrite(LED_PIN, HIGH);
  } else {
    piControl = 0;
    digitalWrite(LED_PIN, LOW);
  }

  // wait until 2 bytes are available, command and length of number
  if (Serial.available() >= 2) {
    /*
     * Commands from RPi should look like (where each <...> is one byte): 
     * <Servo to control T/S> <number of digits to read n> <digit 1> ... <digit n>
     * e.g. to set steering servo to a pulse width of 1500us: S41500
     * e.g. to set throttle servo to a pulse width of 750us: T3750
     */
    command = Serial.read();
    len = Serial.read() - '0';

    // wait for all digits to be written into buffer
    while (Serial.available() < len);

    pulse = 0;
    for (int i=0; i<len; ++i) {
      pulse *= 10;
      pulse += (Serial.read() - '0');
    }
    
    if (piControl) {
      if (command == THROTTLE_COMMAND) {
        throttle.writeMicroseconds(pulse);
      } else if (command == STEERING_COMMAND) {
        steering.writeMicroseconds(pulse);
      }
    }
  }

  // moving average of last 10 readings for steering and throttle signals
  s_total -= s_readings[index];
  s_readings[index] = pulseIn(STEERING_IN, HIGH, 40000);
  s_total += s_readings[index];
  t_total -= t_readings[index];
  t_readings[index] = pulseIn(THROTTLE_IN, HIGH, 40000);
  t_total += t_readings[index];
  if (++index >= NUM_READINGS) {
    index = 0;
  }
  
  if (!piControl) {
    throttle.writeMicroseconds(t_total/NUM_READINGS);
    steering.writeMicroseconds(s_total/NUM_READINGS);
  }
}

