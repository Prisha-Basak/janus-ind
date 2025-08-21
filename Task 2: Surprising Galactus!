//Name: Prisha Basak
//Student ID: 2025A8PS1075H

//pin connections
const int forcepin = A0;      //force sensor
const int ascendled = 2;    //LED for ascending cz we up ong (green)
const int apogeeled = 3;    //LED for apogee cz peaking is lame anyway (yellow)
const int descendled = 4;   //LED for descending cz syndrome down (red)
const int buzzer = 5;       //piezo buzzer cz loud noise is cool :D

//variables
int prevforce = 0;
int currentforce = 0;
int state = 0; 
//0 = starting state, 1 = ascending, 2 = apogee, 3 = descending
int laststate = 0; 

const int threshold = 10;

void setup(){
  pinMode(ascendled, OUTPUT);
  pinMode(apogeeled, OUTPUT);
  pinMode(descendled, OUTPUT);
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);
}

void loop(){
  currentforce = analogRead(forcepin);

  //to check whether we're moving or nah
  int delta = currentforce - prevforce;

  if (abs(delta) < threshold){
    //to ignore noise
    delta = 0;
  }

  if (delta > 0){
    //force increasing = ascending
    state = 1;
  } else if (delta < 0){
    //force decreasing = descending
    state = 3;
  } else {
    //no change = apogee
    state = 2;
  }
  
  //only update leds and buzzer if change detected
  if (state != laststate){
    updateIndicators(state);
    laststate = state;
  }

  prevforce = currentforce;
  delay(200); 
}

void updateIndicators(int s){
  digitalWrite(ascendled, LOW);
  digitalWrite(apogeeled, LOW);
  digitalWrite(descendled, LOW);
  digitalWrite(buzzer, LOW);

  switch (s) {
    case 1: //ascending
      digitalWrite(ascendled, HIGH);
      break;
    case 2: //apogee
      digitalWrite(apogeeled, HIGH);
      tone(buzzer, 1000, 300); //buzzing at 1kHz for 300ms
      break;
    case 3: //descending
      digitalWrite(descendled, HIGH);
      break;
  }
}
