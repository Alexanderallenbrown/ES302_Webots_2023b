#include <Servo.h>

Servo m1;
Servo m2;
Servo m3;

int16_t m1Command = 90;
int16_t m2Command = 90;
int16_t m3Command = 90;


void setup() {
  // attach servos on requisite pins
  m1.attach(11);
  m2.attach(10);
  m3.attach(9);

  //begin Serial communication
  Serial.begin(115200);
}

void loop() {


  //read commands from Serial
  while(Serial.available()>0){
    
    if(Serial.read()=='!'){
      m1Command = Serial.parseInt();
      m2Command = Serial.parseInt();
      m3Command = Serial.parseInt();
      //now send feedback
      Serial.print(m1Command);
      Serial.print(",");
      Serial.print(m2Command);
      Serial.print(",");
      Serial.print(m3Command);
      Serial.println();
      }
      
    }
    //now send commands
    m1.write(m1Command);
    m2.write(m2Command);
    m3.write(m3Command);

  }
  
  
