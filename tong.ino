#include <Firebase_ESP_Client.h>
#include <WiFi.h>
//Provide the token generation process info.
#include <addons/TokenHelper.h>

// Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

// Provide my wifi contain ID and Password
#define WIFI_SSID "Lab 307"
#define WIFI_PASSWORD "307307307"

// Insert Firebase project API Key
#define API_KEY "O1UCPJb4lulFVUBsJyEaV4nlnCVmbUdUxzR696KD"

/* Define the RTDB URL */
#define DATABASE_URL "https://svstartup-5c433-default-rtdb.firebaseio.com/"

// define Firebase data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

#include <Wire.h>
#include <JY901.h>
unsigned long sendDataPrevMillis = 0;
bool signupOK = false;
int n = 1;;
#define coi 27
#define led 14

#define Direction_Wind 19 // direction sensor pin
#define READ_TIME 1000 //ms
#define WIND_SENSOR_PIN 15 //wind sensor pin
#define WIND_SPEED_20_PULSE_SECOND 1.75  //in m/s this value depend on the sensor type
#define ONE_ROTATION_SENSOR 20.0
volatile unsigned long Rotations; //Cup rotation counter used in interrupt routine

float WindSpeed; //Speed meter per second

unsigned long gulStart_Read_Timer = 0;
// prototype function
void speedWind();
void isr_rotation();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WI-FI");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP:");
  Serial.println(WiFi.localIP());
  Serial.println();

  // assign the api key (required)
  config.api_key = API_KEY;
  // assign the RTDB URL (required)
  config.database_url = DATABASE_URL;
  // sign up
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("signUp OK");
    digitalWrite(coi, HIGH);
    delay(100);
    digitalWrite(coi, LOW);
    signupOK = true;
  }
  else {
    Serial.println("%s\n");
  }
  // Assign the callback function for the long running token generation task
  config.token_status_callback = tokenStatusCallback;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
  pinMode(coi, OUTPUT);

  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
  // start protocol I2C with sensor JY901
  JY901.startIIC();
  // JY901.GetTime();
  pinMode(WIND_SENSOR_PIN, INPUT_PULLUP);
  //Set up the interrupt
  attachInterrupt(digitalPinToInterrupt(WIND_SENSOR_PIN), isr_rotation, CHANGE); 
  sei(); //Enables interrupts
  gulStart_Read_Timer - millis();
}
//void jy901() {
//  for (int i = 0; i < 50; i++) {
//    //Angle
//    float x1 = (float)JY901.stcAngle.Angle[0] / 32768 * 180;
//    float y1 = (float)JY901.stcAngle.Angle[1] / 32768 * 180;
//    float z1 = (float)JY901.stcAngle.Angle[2] / 32768 * 180;
//    //Acc
//    float x2 = (float)JY901.stcAcc.a[0] / 32768 * 16;
//    float y2 = (float)JY901.stcAcc.a[1] / 32768 * 16;
//    float z2 = (float)JY901.stcAcc.a[2] / 32768 * 16;
//    //Gyro
//    float x3 = (float)JY901.stcGyro.w[0] / 32768 * 2000;
//    float y3 = (float)JY901.stcGyro.w[1] / 32768 * 2000;
//    float z3 = (float)JY901.stcGyro.w[2] / 32768 * 2000;
//
//  }
//}
void loop() {
  // put your main code here, to run repeatedly:
  //speedWind();
  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 5000  || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();
    // JY901.GetAngle();
    float x1 = (float)JY901.getRoll();
    float y1 = (float)JY901.getPitch();
    float z1 = (float)JY901.getYaw();
    //Acc
    //JY901.GetAcc();
    float x2 = (float)JY901.getAccX() ;
    float y2 = (float)JY901.getAccY() ;
    float z2 = (float)JY901.getAccZ() ;
    //Gyro
    //JY901.GetGyro();
    float x3 = (float)JY901.getGyroX();
    float y3 = (float)JY901.getGyroY();
    float z3 = (float)JY901.getGyroZ();
    float sensor = analogRead(19);
    float voltage1 = sensor * 5 / 1023;
    int direction_wind = map(sensor, 0, 1023, 0, 360);
    cli(); //Disable interrupts
    WindSpeed = WIND_SPEED_20_PULSE_SECOND / ONE_ROTATION_SENSOR * (float)Rotations;
    //Serial.println(WindSpeed);
    sei(); //Enables interrupts
    Rotations = 0;
    if (Firebase.RTDB.set(&fbdo, "/COT1/Angle/X", x1) && Firebase.RTDB.set(&fbdo, "/COT1/Angle/Y", y1) && Firebase.RTDB.set(&fbdo, "/COT1/Angle/Z", z1) && Firebase.RTDB.set(&fbdo, "/COT1/SPEED", WindSpeed) && Firebase.RTDB.set(&fbdo, "/COT1/DIRECTION", direction_wind) && Firebase.RTDB.set(&fbdo, "/COT1/Acc/X", x2) && Firebase.RTDB.set(&fbdo, "/COT1/Acc/Y", y2) && Firebase.RTDB.set(&fbdo, "/COT1/Acc/Z", z2) && Firebase.RTDB.set(&fbdo, "/COT1/Gyro/X", x3) && Firebase.RTDB.set(&fbdo, "/COT1/Gyro/Y", y3) && Firebase.RTDB.set(&fbdo, "/COT1/Gyro/Z", z3)) {
      //      Serial.print("x:");
      //      Serial.println(x1);
      //      Serial.print("y:");
      //      Serial.println(y1);
      //      Serial.print("z:");
      //      Serial.println(z1);
      digitalWrite(coi, HIGH);
      delay(100);
      digitalWrite(coi, LOW);
      Serial.print("SPEED:");
      Serial.println(WindSpeed);
      //      Serial.print("DIRECTION:");
      //Serial.println(direction_wind);
      Serial.println();
    }
    else {
      Serial.println("FAILED: " + fbdo.errorReason());
    }
  }
  //      Serial.print("SPEED:");
  //      Serial.println(WindSpeed);
}
void speedWind()
{
  if ((millis() - gulStart_Read_Timer) >= READ_TIME)
  {
    cli(); //Disable interrupts
    WindSpeed = WIND_SPEED_20_PULSE_SECOND / ONE_ROTATION_SENSOR * (float)Rotations;
    Serial.println(WindSpeed);
    sei(); //Enables interrupts
    Rotations = 0;
    gulStart_Read_Timer = millis();
  }
}
////// This is the function that the interrupt calls to increment the rotation count
void isr_rotation()
{
  Rotations++;
}
