#include <cvzone.h>

SerialData serialData(1, 1); //(numOfValsRec,digitsPerValRec)
int valsRec[1]; // array of int with size numOfValsRec 

void setup() {
  pinMode(10, OUTPUT); // Pin for green LED
  pinMode(13, OUTPUT); // Pin for red LED
  serialData.begin();
}

void loop() {
  serialData.Get(valsRec);

  if (valsRec[0] == 1) {
    // Vehicle detected, turn on the green LED
    digitalWrite(10, HIGH);
    digitalWrite(13, LOW); // Turn off the red LED
  } else if (valsRec[0] == 0) {
    // No vehicle detected, turn on the red LED
    digitalWrite(10, LOW); // Turn off the green LED
    digitalWrite(13, HIGH);
  } else if (valsRec[0] == 2) {
    // Exit
    digitalWrite(10, LOW); 
    digitalWrite(13, LOW);
  }

  delay(10);
}
