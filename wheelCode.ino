int sensor = A0;

void setup() {
  // put your setup code here, to run once:
  pinMode(sensor, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue = analogRead(sensor);

  Serial.println(sensorValue);
  delay(10);
  
}
