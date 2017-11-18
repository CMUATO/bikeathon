int hallPin = A0;
int circ = 0.0031566; //In miles
int prevState = HIGH;
double distance = 0.0;
int count = 0;
int numZeros = 0;

int prevTime = millis();

void setup() {
  pinMode(hallPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int state = analogRead(hallPin);
//  Serial.println(state);
  if(state == 0 && prevState > 500){
    
    int currentTime = millis();
    if(currentTime - prevTime > 100) {
      count += 1;
      Serial.println(count);
      prevTime = currentTime;
    }
  }
  prevState = state;

}
