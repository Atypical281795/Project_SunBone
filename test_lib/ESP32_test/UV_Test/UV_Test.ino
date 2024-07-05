int ultra;
void setup() 
{
  Serial.begin(9600);
  pinMode(14,OUTPUT);
  digitalWrite(14,HIGH);
}
 
void loop() 
{
  ultra=analogRead(14)/4;
  Serial.println(ultra);
  delay(500);
  if(ultra>600){
    Serial.println("紫外線過量");
  }
}