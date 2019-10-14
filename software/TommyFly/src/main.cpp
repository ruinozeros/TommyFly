#include <Arduino.h>
#include "MS5611.h"
#include "Queue.h"

MS5611 baro;
int32_t pressure;
float filtered = 0;
float mtr;
float ref = 0;

#define POINTS_PER_INTERVALL 100
#define INTERVALL_MS 300

#define THRESHOLD_FLOAT_MED  0.12
#define THRESHOLD_FLOAT_SLOW 0.08

RingQueue<float, POINTS_PER_INTERVALL> window;

void setup() {
  baro = MS5611();
  baro.begin();

  Serial.begin(9600);
  delay(2000);
}

int iteration = 0;
float moving_average_old = 0.0;

void loop() {
    // Read pressure
  pressure = baro.getPressure();
  
  if(filtered != 0){
    filtered = filtered + 0.05*(pressure-filtered);
  }
  else {
    filtered = pressure;          // first reading so set filtered to reading
  }
  if(ref == 0){
    ref = filtered/12.0;
  }
  
  mtr = ref - filtered/12.0;
  
  // Send pressure via serial (UART);
  // Serial.println(mtr);

  if(window.length() == 100) {
    window.pop();
  }

  window.push(mtr);
  
  iteration = (iteration + 1) % 30;

  if (iteration == 0) {
      float moving_average = window.sum() / window.length();
      float speed = moving_average - moving_average_old;
      Serial.print(speed);
      Serial.print("m pro intervall\t");
      moving_average_old = moving_average;

      // rising
      if(speed > THRESHOLD_FLOAT_SLOW && speed < THRESHOLD_FLOAT_MED) {
        Serial.print("up");
      }
      else if(speed > THRESHOLD_FLOAT_MED) {
        Serial.print("UP");
      }
      else if(speed < THRESHOLD_FLOAT_SLOW * -1.0 && speed > THRESHOLD_FLOAT_MED * -1.0) {
        Serial.print("down");
      }
      else if(speed < THRESHOLD_FLOAT_MED * -1.0) {
        Serial.print("DOWN");
      }
      

      Serial.println("");
  }

  unsigned long interval = INTERVALL_MS / POINTS_PER_INTERVALL;
  delay(interval); 
}