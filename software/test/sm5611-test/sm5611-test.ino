#include <MS5611.h>

MS5611 baro;
int32_t pressure;
float filtered = 0;
float mtr;
float ref = 0;


void setup() {
  // Start barometer
  baro = MS5611();
  baro.begin();
  // Start serial (UART)
  Serial.begin(9600);
  delay(2000);

}

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
  Serial.println(mtr);
  delay(10); 
}
