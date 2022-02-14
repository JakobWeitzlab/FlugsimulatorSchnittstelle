#include <Joystick.h>
#include <Wire.h>

Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, 
  JOYSTICK_TYPE_JOYSTICK, 0, 0,
  true, true, true, false, false, false,
  false, false, false, false, false);

//setting the sendmode -> autoSend for constant sending of the values
const bool testAutoSendMode = true;

int xAxis_ = 0;
int yAxis_ = 0;
int zAxis_ = 0;
int degree;
int select;
int received;

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
    received = Wire.read();
    if (received == 0x5B)
    {
      //select = received;
      degree = Wire.read();
      Joystick.setXAxis(511.5 + (degree*5.68));
    }
    else if(received == 0x5C)
    {
      //select = received;
      degree = Wire.read();
      Joystick.setXAxis(degree*5.68);
    }    
    else if(received == 0x5D)
    {
      //select = received;
      degree = Wire.read();
      Joystick.setXAxis(511.5 + (degree*5.68));
    }
    else if(received == 0x5E)
    {
      //select = received;
      degree = Wire.read();
      Joystick.setXAxis(degree*5.68);
    }
    else if(received == 0x5F)
    {
      //select = received;
      degree = Wire.read();
      Joystick.setXAxis(511.5 + (degree*5.68));
    }
    else if(received == 0x60)
    {
      //select = received;
      degree = Wire.read();
      Joystick.setXAxis(degree*5.68);
    }
    
  }
      //SelectType(select, degree);
}
