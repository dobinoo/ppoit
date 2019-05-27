 #include<Servo.h>
Servo mot;
Servo steer;

  
  int servo_in=3;
  int servo_out=10;
  int motor_in=6;
  int motor_out=9;
  int motor_value;
  int servo_value;
  int trigPin = 13;    
  int echoPin = 12;    
  int light= A0;
  int light_value = 0;
  int led1=4;
  int led2=2;
  long cm;
  String message;
  //0 % steer 1436  dolava 1733 doprava 1138
  //0% motor 1500  100% 1770 -100% 1196

void setup() {
  mot.attach(9);
  steer.attach(10);
  pinMode(servo_out, OUTPUT);
  pinMode(motor_out, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(5, INPUT);        //IR sensor1
  pinMode(7, INPUT);        //IR sensor2
  Serial.begin(115200);
}

void loop() {

  Serial.begin(115200);
  if (Serial.available() )
    {
         message=Serial.readStringUntil('R'); 
         for(int i=0;i<13;i++)
          {
            Serial.print(message[i]);
          } 
         Serial.end();                                           
    }

  if (message[0]=='0')   // auto off motory a steer na 0 % 
    {
      mot.writeMicroseconds(1500);
      steer.writeMicroseconds(1436);
      
    }
  
  if (message[0]=='1')                             // AUTO ON 
    {            
      if  (message[2]=='0')                             // Manual svetla
        {
          if  (message[1]=='0')                             // Svetla manual OFF 
            {
              LIGHT_MANUAL_OFF();
            }
          if  (message[1]=='1')                           // Svetla manual ON 
            {
              LIGHT_MANUAL_ON();
            }
        }

      if  (message[2]=='1')                               // Svetla AUTO
        {
          light_value=LIGHT_AUTO();                     // Vracia nameranu intenzitu svetla
        }

      if  (message[3]=='0')                               // LANE ASSIST OFF
        {
          
        }
      if  (message[3]=='1')                               // LANE ASSIST ON
        {
          LANE_ASSIST();
          motor_value = pulseIn(motor_in, HIGH);
          mot.writeMicroseconds(motor_value);
        }
      if  (message[4]=='0')                               // ADDAPTIVE CRUISE CONTROL OFF
        {
          
        }
      if  (message[4]=='1')                               // ADDAPTIVE CRUISE CONTROL ON
        { 
          ADAPTIVE_CRUISE_CONTROL(MEASURED_DISTANCE()); 
          servo_value = pulseIn(servo_in, HIGH);
          steer.writeMicroseconds(servo_value); 
        }
      if  (message[5]=='0' and message[4]=='0' and message[3]=='0')                                 // CAR CONTROL 
        {
          MANUAL_CONTROL();                                                 // REMOTE CONTROL
        }
      if  (message[5]=='1' and message[4]=='0' and message[3]=='0')
        {
          motor_value=(message[6]-'0')*100+(message[7]-'0')*10+(message[8]-'0');
          servo_value=(message[9]-'0')*100+(message[10]-'0')*10+(message[11]-'0');
          Serial.print("motor:");
          Serial.println(motor_value);
          Serial.print("servo:");
          Serial.println(servo_value);
          Serial.println("upravene");
          motor_value=map(motor_value,0,100,1500,1770);
          servo_value=map(servo_value,0,100,1770,1138);
          Serial.println();
          Serial.print("motor:");
          Serial.println(motor_value);
          Serial.print("servo:");
          Serial.println(servo_value);
          WEB_CONTROL(servo_value, motor_value);                  // WEB CONTROL
          
          
          
        }
  

            

 


  
    }

  
    
 delay(10);

}

int LIGHT_AUTO()
{
  {
    int light_value1;
    light_value1 = analogRead(light);
    if (light_value1<850)  // viac svetla vačšia hodnota 1000 ked nato svietim mobilom 
      {
        digitalWrite(led1, HIGH);
        digitalWrite(led2, HIGH);
      }
    else
      {
         digitalWrite(led1, LOW);
         digitalWrite(led2, LOW);
      }
//  Serial.println(light_value);
    return light_value1;  
  }
}

void LIGHT_MANUAL_ON()
{
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
}

void LIGHT_MANUAL_OFF()
{
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);  
}

void ADAPTIVE_CRUISE_CONTROL(long cmm)
{
  int zelana_vzdialenost=10;
  int error;
  error=cmm-zelana_vzdialenost;
  float Kp=3.5;
  int drive;
  float P;
  P=error*Kp;
  drive=1500+P;
  if (drive>1560)
    {
      drive=1560;
    }
  if (drive<1400)
    {
      drive=1400;
    }
    mot.writeMicroseconds(drive);
  
  
      
    
}

long MEASURED_DISTANCE()
{
  long duration;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  //Serial.print((duration/2) / 29.1);
  //Serial.print("cm");
  //Serial.println();
 
  
  return ( (duration/2) / 29.1);
}

void MANUAL_CONTROL()
{
   servo_value = pulseIn(servo_in, HIGH);
   motor_value = pulseIn(motor_in, HIGH);
   mot.writeMicroseconds(motor_value);
   steer.writeMicroseconds(servo_value); 
   // Serial.println();
   // Serial.print("servo:");
   // Serial.print(servo_value);
   // Serial.print("    motor:");
   // Serial.println(motor_value);
}

void WEB_CONTROL(int servo_web, int motor_web)
{
   if(motor_web>=1700)
    {
      motor_web=1700;       // Vykonove obmedzenie
    }
   mot.writeMicroseconds(motor_web);
   steer.writeMicroseconds(servo_web);
}


void LANE_ASSIST()
{
  if (digitalRead(5)and digitalRead(7)==0)       //zaboc doprava
    {
        steer.writeMicroseconds(1700); 
    }
  if (digitalRead(7) and digitalRead(5)==0)       //dolava
    {
        steer.writeMicroseconds(1150); 
    }
    if (digitalRead(7)==0 and digitalRead(5)==0)
      {
        steer.writeMicroseconds(1436);
      }
  
}
