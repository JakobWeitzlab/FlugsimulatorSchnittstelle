#include <Joystick.h>
#include <Wire.h>

Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, 
  JOYSTICK_TYPE_JOYSTICK, 0, 0,
  true, true, false, false, false, false,
  true, false, false, false, false);

//setting the sendmode -> autoSend for constant sending of the values
const bool testAutoSendMode = true;

int xAxis_ = 0;
int yAxis_ = 0;
int zAxis_ = 0;
int degree;
int select;
int identifier;

void setup() {

  Joystick.begin();
  Wire.begin(0x03);
  Wire.onReceive(ReceiveEvent);  //register event
  Serial.begin(9600); //starts a serial connection at 9600bps
  
}

void loop() {
  //delay(1000);
}

void SelectType(int select1, int degree1) {
  switch(select1){
    case 0x5B:
      Joystick.setXAxis(511.5 + (degree1*5.68));
     break;
    case 0x5C:
      Joystick.setXAxis(degree1*5.68);
     break;
    case 0x5D:
      Joystick.setYAxis(511.5 + (degree1*5.68));
     break;
    case 0x5E:
      Joystick.setYAxis(degree1*5.68);
     break;
    case 0x5F:
      Joystick.setZAxis(511.5 + (degree1*5.68));
     break;
    case 0x60:
      Joystick.setZAxis(degree1*5.68);
     break;
  }
  //delay(10);
}

void ReceiveEvent(int howMany){
  while (Wire.available())
  {
    identifier = Wire.read();
    if (identifier == 0x5B)
    {
      degree = Wire.read();
      Joystick.setXAxis(511.5 + (degree*5.68));
      Serial.println(degree);
    }
    else if(identifier == 0x5C)
    {
      degree = Wire.read();
      Joystick.setXAxis(degree*5.68);
      Serial.println(degree);
    }    
    else if(identifier == 0x5D)
    {
      degree = Wire.read();
      Joystick.setYAxis(511.5 + (degree*5.68));
    }
    else if(identifier == 0x5E)
    {
      degree = Wire.read();
      Joystick.setYAxis(degree*5.68);
    }
    else if(identifier == 0x5F)
    {
      degree = Wire.read();
      Joystick.setRudder(511.5 + (degree*5.68));
    }
    else if(identifier == 0x60)
    {
      degree = Wire.read();
      Joystick.setRudder(degree*5.68);
    }
    
  }
      delay(100);
      //SelectType(select, degree);
}
