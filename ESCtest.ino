#include <Servo.h>
Servo throttle;
Servo steer;
int throttleRead = 7;
int steerRead = 8;
unsigned long Tduration;
unsigned long Sduration;
int ledPin = 13;
void setup()
{
  Serial.begin(115200);
  pinMode(throttleRead, INPUT);
  pinMode(steerRead, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  throttle.attach(9);
  steer.attach(10);
}

void loop()
{
  Tduration = pulseIn(throttleRead, HIGH, 20000);
  if (Tduration > 100) {
    throttle.writeMicroseconds(Tduration);
  } else {
    throttle.writeMicroseconds(1500);
  }
  Sduration = pulseIn(steerRead, HIGH, 20000);
  if (Sduration > 100) {
    steer.writeMicroseconds(Sduration);
  } else {
    steer.writeMicroseconds(1500);
  }
  Serial.print(Tduration);
  Serial.write(" : ");
  Serial.print(Sduration);
  Serial.println();
}

