int ledPin = 13;
int ledState=0;
void setup()
{
  Serial.begin(115200); 
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
 } 

void loop()
{
  if (ledState==1)
  {
     digitalWrite(ledPin, 1);
     delay(500);   
     digitalWrite(ledPin, 0);
     ledState=0;
  }
} 

void serialEvent()
{
  Serial.read();
  ledState=1;
}
