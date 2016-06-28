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
#define END_SWITCH 4

Servo throttle;
Servo steering;
unsigned long switchPulse;
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
  Serial.begin(115200);
  pinMode(THROTTLE_IN, INPUT);
  pinMode(STEERING_IN, INPUT);
  pinMode(SWITCH_IN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  pinMode(END_SWITCH, INPUT_PULLUP);
  throttle.attach(THROTTLE_OUT);
  steering.attach(STEERING_OUT);
  index = 0;
  s_total = 0;
  t_total = 0;
  for (int i=0; i<NUM_READINGS; ++i) {
    s_readings[i] = 0;
    t_readings[i] = 0;
  }
  throttle.writeMicroseconds(1500);
  steering.writeMicroseconds(1500);
}

void loop() {
  // if controller switch is on, pi has control
  switchPulse = pulseIn(SWITCH_IN, HIGH, 40000);
  if (switchPulse > 1800 || switchPulse == 0) {
    piControl = 1;
    digitalWrite(LED_PIN, HIGH);
  } else if (switchPulse > 1200) {
    piControl = 2;
    digitalWrite(LED_PIN, LOW);
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

    if (pulse < 1000) {
      pulse = 1000;
    } else if (pulse > 2000){
      pulse = 2000;
    }
    
    if (piControl) {
      if (command == THROTTLE_COMMAND && piControl != 2) {
          throttle.writeMicroseconds(pulse);
      } else if (command == STEERING_COMMAND) {
        steering.writeMicroseconds(pulse);
      }
    }
  }

  // moving average of last 10 readings for steering and throttle signals
  s_total -= s_readings[index];
  s_readings[index] = pulseIn(STEERING_IN, HIGH, 40000);
  if (s_readings[index] < 1000) {
    s_readings[index] = 1500;
  }
  s_total += s_readings[index];
  
  t_total -= t_readings[index];
  t_readings[index] = pulseIn(THROTTLE_IN, HIGH, 40000);
  if (t_readings[index] < 1000) {
    t_readings[index] = 1500;
  }
  t_total += t_readings[index];
  
  if (++index >= NUM_READINGS) {
    index = 0;
  }
  
  if (!piControl) {
    throttle.writeMicroseconds(t_total/NUM_READINGS);
    steering.writeMicroseconds(s_total/NUM_READINGS);
  } else if (piControl == 2) {
    throttle.writeMicroseconds(t_total/NUM_READINGS);
  }
}

