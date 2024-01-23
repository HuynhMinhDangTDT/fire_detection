#include <DFRobotDFPlayerMini.h>
#include <WiFi.h>
#include "DHT.h"
#include <aht_sim800.h>
#define MODEM_RX 9
#define MODEM_TX 10
#define uart Serial1

AHT_GSM *gsmMaster = new AHT_GSM(&uart);
AHT_GSM *gsm;
GSM_TYPE gsmType;
bool gsmOk = false;

//HardwareSerial Serial2(1);

DFRobotDFPlayerMini myPlayer;

const char* ssid = "VIRUS";
const char* password = "bat3glen";

const uint16_t port = 8090;
const char * host = "192.168.1.19";

// String number1 = "0907586421";// nhap sdt vào đây

WiFiServer wifiServer(8090);

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

//#define Den_bao_chay 15;
// #define RXD1 0         // GPIO 16 => RX for uart
// #define TXD1 4        // GPIO 17 => TX for uart
#define RXD2 16         // GPIO 16 => RX for uart
#define TXD2 17         // GPIO 17 => TX for uart
#define IN3_cua 18
#define IN4_cua 19
#define ENB_cua 15
#define rain_sensor 5
// #define nut_reset 32
#define Den_bao_dong 21
#define Den_bao_chua_chay 0
#define analog_quangtro 34
#define cam_bien_can_1 23
#define cam_bien_can_2 22
#define trigPin 25
#define echoPin 26

int mode_bao_dong = 0;
int mode_dieu_khien = 0;
int hoat_dong = 0;
int loa_bao_trom = 0;
int count_am_thanh_co_trom = 0;
int loa_bao_mo_gieng = 0;
int loa_bao_dong_gieng = 0;
int loa_bao_dong_gieng_mua = 0;
int last_gia_tri_Quang_tro = 0;
int last_gia_tri_cam_bien_mua = 0;
int status_gieng = 0;


String stringOne = String("");
String stringTwo = String("");
String canh_bao_trom = String("");
String data_sim = String("");

//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
float distanceInch;


void setup(){
  // put your setup code here, to run once:
  Serial.begin(115200);

  // uart.begin(9600, SERIAL_8N1, RXD1, TXD1);
  // Serial.begin(115200);
    delay(30000);

    if(gsmMaster->begin()) 
    {
        gsmType = gsmMaster->detectGSM(&uart);
        unsigned long baudrate = gsmMaster->getBaudrate();
        free(gsmMaster);
        
        if(gsmType == SIM800) 
        {
            gsm = new AHT_SIM800(&uart);
            gsm->begin(baudrate);
            gsmOk = true;
        }

        delay(5000);
        uart.println("AT+CMGF=1");
        update_load();
        delay(1000);  // Delay of 1 second
        uart.println("AT+CNMI=1,2,0,0,0"); // Decides how newly arrived SMS messages should be handled
        delay(1000);
        update_load();
        uart.println((char)26);// ASCII code of CTRL+Z for saying the end of sms to  the module 
        update_load();
    }
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
  pinMode(Den_bao_dong, OUTPUT);
  pinMode(Den_bao_chua_chay, OUTPUT);
  pinMode(rain_sensor, INPUT);
  // pinMode(nut_reset, INPUT);
  pinMode(cam_bien_can_1, INPUT);
  pinMode(cam_bien_can_2, INPUT);
  pinMode(IN3_cua, OUTPUT);
  pinMode(IN4_cua, OUTPUT);
  pinMode(ENB_cua, OUTPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  dht.begin();

  if(!myPlayer.begin(Serial2)){
    Serial.println("Unable to begin");
  }

  myPlayer.volume(100);
  //  myPlayer.play(1);
  delay(1000);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");
  Serial.println(WiFi.localIP());
  wifiServer.begin();
  
  Serial.println("Initializing....");
  digitalWrite(Den_bao_dong, LOW);
  analogWrite(Den_bao_chua_chay, 0);
  // uart.println("AT"); //Once the handshake test is successful, it will back to OK
  // // updateSerial();
  // uart.println("AT+CMGF=1"); // Configuring TEXT mode
  // updateSerial();
  // // uart.println("AT+CNMI=1,2,0,0,0"); // Decides how newly arrived SMS messages should be handled
  // Serial.println("AT+CNMI=2,2,0,0,0"); // AT Command to receive a live SMS
  // updateSerial();
  // // uart.println("AT");
  // delay(3000);
  // uart.println("AT+CMGF=1");
  // delay(1000);
  //  initModule("AT", "OK", 1000);              //Once the handshake test is successful, it will back to OK
  
}


void update_load(){
  if(!gsmOk)
    {
        Serial.println("can't detect gsm module");
        delay(5000);
        return;
    }

    if(uart.available())
    {
        // Serial.println(uart.readString());
        String sms = uart.readString();
        // String message1 = sms.substring(84);
        String message1 = sms.substring(48);
        Serial.println("messge sms: " + sms);
        Serial.println("Message is :" + message1 );
        if (isStringInString("Dong", message1)){
          // Serial.println("String found in the string.");
          Serial.println("Dong");
          dong_gieng();
          for(int i = 0; i <20000;i++){
            Serial.print(i);
            dong_gieng();
            // dong_gieng();
            if (status_gieng = 2){
              if(digitalRead(cam_bien_can_2) == HIGH){
                // Serial.println("motor mo gieng dang dung");
                digitalWrite(IN3_cua, LOW);
                digitalWrite(IN4_cua, LOW);
              }
              status_gieng = 0;
            }
          }
        }
        if (isStringInString("Mo", message1)){
          Serial.println("Mo");
          Serial.println("mo_gieng boi dien thoai");
          mo_gieng();
          for(int i = 0; i <20000;i++){
            Serial.print(i);
            mo_gieng();
            // dong_gieng();
            if (status_gieng = 1){
              if(digitalRead(cam_bien_can_1) == HIGH){
                // Serial.println("motor mo gieng dang dung");
                digitalWrite(IN3_cua, LOW);
                digitalWrite(IN4_cua, LOW);
              }
              status_gieng = 0;
            }
          }
        }
        // if (isStringInString("0044006F006E0067", message1)){
        //   // Serial.println("String found in the string.");
        //   Serial.println("Dong");
        //   dong_gieng();
        //   for(int i = 0; i <20000;i++){
        //     Serial.print(i);
        //     dong_gieng();
        //     // dong_gieng();
        //     if (status_gieng = 2){
        //       if(digitalRead(cam_bien_can_2) == HIGH){
        //         // Serial.println("motor mo gieng dang dung");
        //         digitalWrite(IN3_cua, LOW);
        //         digitalWrite(IN4_cua, LOW);
        //       }
        //       status_gieng = 0;
        //     }
        //   }
        // }
        // if (isStringInString("004D006F", message1)){
        //   Serial.println("Mo");
        //   Serial.println("mo_gieng boi dien thoai");
        //   mo_gieng();
        //   for(int i = 0; i <20000;i++){
        //     Serial.print(i);
        //     mo_gieng();
        //     // dong_gieng();
        //     if (status_gieng = 1){
        //       if(digitalRead(cam_bien_can_1) == HIGH){
        //         // Serial.println("motor mo gieng dang dung");
        //         digitalWrite(IN3_cua, LOW);
        //         digitalWrite(IN4_cua, LOW);
        //       }
        //       status_gieng = 0;
        //     }
        //   }
        // }
        // String sms = uart.readString();
        // 
        // ASCIIValue now contain "TEST"
        
        // String message1 = sms.substring(48);
        // String asciiString = hexStringToASCII(message1);
        // Serial.println(asciiString);
    }
    if(Serial.available())
    {
        char c = Serial.read();
        Serial.write(c);
        uart.write(c);
    }
}

bool isStringInString(String target, String str) {
  return str.indexOf(target) != -1;
}

// const String number1 = "+9779800990088";
// const String number2 = ""; //optional
// const String PHONE_3 = ""; //optional

// void callUp(char *number) {
//   uart.print("ATD + "); uart.print(number); uart.println(";"); //Call to the specific number, ends with semi-colon,replace X with mobile number
//   delay(20000);       // wait for 20 seconds...
//   uart.println("ATH"); //hang up
//   delay(100);
// }


void initModule(String cmd, char *res, int t){
  while(1){
  //    Serial.println(cmd);
    Serial.println(cmd);
    delay(100);
    while (uart.available() > 0) {
      if (uart.find(res)) {
        Serial.println(res);
        delay(t);
        return;
      } else {
        Serial.println("Error");
      }
    }
    delay(t);
  }
}


void mo_gieng(){
  // Serial.println("cam bien 1");
  // Serial.println(digitalRead(cam_bien_can_1));
  status_gieng = 1;
  if(digitalRead(cam_bien_can_1) == HIGH){
    // Serial.println("motor mo gieng dang dung");
    digitalWrite(IN3_cua, LOW);
    digitalWrite(IN4_cua, LOW);
  }else
  {
    analogWrite(ENB_cua, 100);
    digitalWrite(IN3_cua, HIGH);
    digitalWrite(IN4_cua, LOW);
  }
}


void dong_gieng(){
  // Serial.println("cam bien 2");
  // Serial.println(digitalRead(cam_bien_can_2));
  status_gieng = 2;
  if(digitalRead(cam_bien_can_2) == HIGH){
    // Serial.println("motor dong gieng dang dung");
    digitalWrite(IN3_cua, LOW);
    digitalWrite(IN4_cua, LOW);
  }else
  {
    analogWrite(ENB_cua, 100);
    digitalWrite(IN4_cua, HIGH);
    digitalWrite(IN3_cua, LOW);
  }
}


// String number1 = "0963432341";// nhap sdt vào đây
// String number2 = "0986050828";// nhap sdt vào đây
String number3 = "0907586421";// nhap sdt vào đây


void send_sms(String text, String phone){
    Serial.println("sending sms....");
    delay(50);
    uart.print("AT+CMGF=1\r");
    delay(1000);
    uart.print("AT+CMGS=\""+phone+"\"\r");
    delay(1000);
    uart.print(text);
    delay(100);
    // sim800L.write(0x1A); //ascii code for ctrl-26 //Serial2.println((char)26); //ascii code for ctrl-26'
    uart.println((char)26);// ASCII code of CTRL+Z
    delay(5000);
}


void make_call(String phone){
    Serial.println("calling....");
    uart.println("ATD"+phone+";");
    delay(20000); //20 sec delay
    uart.println("ATH");
    delay(1000); //1 sec delay
}


void make_multi_call(){
  // if(number1 != ""){
  //   Serial.print("Phone 1: ");
  //   make_call(number1);
  // }
  // if(number2 != ""){
  //   Serial.print("Phone 2: ");
  //   make_call(number2);
  // }
  if(number3 != ""){
    Serial.print("Phone 3: ");
    make_call(number3);
  }
}


void song_am(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculate the distance
  distanceCm = duration * SOUND_SPEED/2;
  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;
}


void check_dung_motor(){
  if (status_gieng = 1){
    if(digitalRead(cam_bien_can_1) == HIGH){
    // Serial.println("motor mo gieng dang dung");
    digitalWrite(IN3_cua, LOW);
    digitalWrite(IN4_cua, LOW);
    }
  }

  if (status_gieng = 2){
    if(digitalRead(cam_bien_can_1) == HIGH){
    // Serial.println("motor mo gieng dang dung");
    digitalWrite(IN3_cua, LOW);
    digitalWrite(IN4_cua, LOW);
    }
  }
}


void check_tin_nhan(){
  // updateSerial();
  while(uart.available()){
    data_sim = uart.readString();
    Serial.println(uart.readString());
    if (data_sim == "m"){
      mo_gieng();
      for(int i = 0; i <20000;i++){
        Serial.print(i);
        mo_gieng();
        // dong_gieng();
        if (status_gieng = 1){
          if(digitalRead(cam_bien_can_1) == HIGH){
            // Serial.println("motor mo gieng dang dung");
            digitalWrite(IN3_cua, LOW);
            digitalWrite(IN4_cua, LOW);
          }
          status_gieng = 0;
        }
      }
    }

    if (data_sim == "d"){
      dong_gieng();
      for(int i = 0; i <20000;i++){
        Serial.print(i);
        dong_gieng();
        // dong_gieng();
        if (status_gieng = 2){
          if(digitalRead(cam_bien_can_2) == HIGH){
            // Serial.println("motor mo gieng dang dung");
            digitalWrite(IN3_cua, LOW);
            digitalWrite(IN4_cua, LOW);
          }
          status_gieng = 0;
        }
      }
    }
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  int giatriQuangtro = analogRead(analog_quangtro);
  int giatricambienmua = digitalRead(rain_sensor);
  float do_am = dht.readHumidity();
  float nhiet_do = dht.readTemperature();
  float f = dht.readTemperature(true);
  float hic = dht.computeHeatIndex(nhiet_do, do_am, false);
  float hif = dht.computeHeatIndex(f, do_am);

  song_am();
  update_load();

  WiFiClient client = wifiServer.available();
  if (client) {
    while (client.connected()) {
      update_load();
      int giatriQuangtro = analogRead(analog_quangtro);
      int giatricambienmua = digitalRead(rain_sensor);
      //Serial.println(giatriQuangtro);
      float do_am = dht.readHumidity();
      float nhiet_do = dht.readTemperature();
      float f = dht.readTemperature(true);
      float hic = dht.computeHeatIndex(nhiet_do, do_am, false);
      float hif = dht.computeHeatIndex(f, do_am);
      String c = client.readString();
      Serial.println(c);
      String string_nhiet_do = String(nhiet_do);
      String string_do_am = String(do_am);
      String string_quang_tro = String(giatriQuangtro);
      String string_cam_bien_mua = String(giatricambienmua);
      String string_cam_bien_song_am = String(distanceCm);
      String string_che_do_dieu_khien = String(mode_dieu_khien);
      stringTwo += stringOne;
      stringTwo += string_nhiet_do;
      stringTwo += ";";
      stringTwo += string_do_am;
      stringTwo += ";";
      stringTwo += string_quang_tro;
      stringTwo += ";";
      stringTwo += string_cam_bien_mua;
      stringTwo += ";";
      stringTwo += string_cam_bien_song_am;
      stringTwo += ";";
      stringTwo += string_che_do_dieu_khien;
      stringTwo += ";";
      // stringTwo += data_sim;
      // stringTwo += ";";
      stringTwo += c;
      stringTwo += ";";
      Serial.println(stringTwo);
      client.print(stringTwo);
      stringOne = "";
      stringTwo = "";


      // check_dung_motor();

      // delay(500);
      if (c == "lua")
      {
        Serial.println("bao chay");
        mode_bao_dong = 1;
      }
      else if (c == "auto")
      {
        Serial.println("che do auto");
        mode_dieu_khien = 0;
      }
      else if (c == "manual")
      {
        Serial.println("che do manual");
        mode_dieu_khien = 1;
      }
      else if (c == "mo")
      {
        Serial.println("mo_gieng boi web");

        mo_gieng();
        for(int i = 0; i <20000;i++){
          Serial.print(i);
          mo_gieng();
          // dong_gieng();
          if (status_gieng = 1){
            if(digitalRead(cam_bien_can_1) == HIGH){
              // Serial.println("motor mo gieng dang dung");
              digitalWrite(IN3_cua, LOW);
              digitalWrite(IN4_cua, LOW);
            }
            status_gieng = 0;
          }
        }
      }
      else if (c == "dong")
      {

        Serial.println("dong_gieng boi web");
        dong_gieng();
        for(int i = 0; i <20000;i++){
          Serial.print(i);
          dong_gieng();
          // dong_gieng();
          if (status_gieng = 2){
            if(digitalRead(cam_bien_can_2) == HIGH){
              // Serial.println("motor mo gieng dang dung");
              digitalWrite(IN3_cua, LOW);
              digitalWrite(IN4_cua, LOW);
            }
            status_gieng = 0;
          }
        }
      }
      update_load();
      // if (c == ""){
      //   break;
      // }
    }
    client.stop();
    Serial.println("Client disconnected");
  }

  if (mode_bao_dong == 0){
    update_load();
    if(mode_dieu_khien == 0){
      update_load();
      if (giatricambienmua == 0 && loa_bao_dong_gieng_mua == 0){
        dong_gieng();
        myPlayer.play(1);
        for(int i = 0; i <20000;i++){
          Serial.print(i);
          // dong_gieng();
          if (status_gieng = 2){
            if(digitalRead(cam_bien_can_2) == HIGH){
              // Serial.println("motor mo gieng dang dung");
              digitalWrite(IN3_cua, LOW);
              digitalWrite(IN4_cua, LOW);
            }
            status_gieng = 0;
          }
          // delay(1000);
          loa_bao_dong_gieng_mua = 1;
          loa_bao_mo_gieng = 0;
        }
      }else if (giatricambienmua == 1){
        loa_bao_dong_gieng_mua = 0;
        if (giatriQuangtro > 1000 && loa_bao_mo_gieng == 0){
          update_load();
          mo_gieng();
          myPlayer.play(3);
          for(int i = 0; i <20000;i++){
            Serial.print(i);
            // mo_gieng();
            if (status_gieng = 1){
              if(digitalRead(cam_bien_can_1) == HIGH){
                // Serial.println("motor mo gieng dang dung");
                digitalWrite(IN3_cua, LOW);
                digitalWrite(IN4_cua, LOW);
              }
              status_gieng = 0;
            }
            // delay(1000);
          }
          loa_bao_mo_gieng = 1;
          loa_bao_dong_gieng = 0;
        }
        else if(giatriQuangtro < 1000 && loa_bao_dong_gieng == 0){
          dong_gieng();
          update_load();
          myPlayer.play(2);
          for(int i = 0; i <20000;i++){
            Serial.print(i);
            // dong_gieng();
            if (status_gieng = 2){
              if(digitalRead(cam_bien_can_2) == HIGH){
                // Serial.println("motor mo gieng dang dung");
                digitalWrite(IN3_cua, LOW);
                digitalWrite(IN4_cua, LOW);
              }
              status_gieng = 0;
            }
            // delay(1000);
          }
          loa_bao_dong_gieng = 1;
          loa_bao_mo_gieng = 0;
        }
      }
    }else{
      loa_bao_dong_gieng_mua = 0;
      loa_bao_dong_gieng = 0;
      loa_bao_mo_gieng = 0;
    }
  }

  if (distanceCm < 26.00){
    dong_gieng();
    if (status_gieng = 2){
      if(digitalRead(cam_bien_can_2) == HIGH){
        // Serial.println("motor mo gieng dang dung");
        digitalWrite(IN3_cua, LOW);
        digitalWrite(IN4_cua, LOW);
      }
      status_gieng = 0;
    }
    mode_bao_dong = 4;
  }

  if (mode_bao_dong == 4){
    dong_gieng();
    count_am_thanh_co_trom += 1;
    // check_dung_motor();
    digitalWrite(Den_bao_dong, HIGH);
    myPlayer.play(4);
    for(int i = 0; i <20000;i++){
      Serial.print(i);
      dong_gieng();
    }
    if (count_am_thanh_co_trom > 2){
      mode_bao_dong = 5; 
    }
  }

  while (mode_bao_dong == 5){
    dong_gieng();
    make_multi_call();
    mode_bao_dong = 6;
  }

  while (mode_bao_dong == 6){
    dong_gieng();
    // if(number1 != ""){
    //   Serial.print("Phone 1: ");
    //   send_sms("Nha dang co ke dot nhap. Goi 113 gap!!!", number1);
    // }
    // if(number2 != ""){
    //   Serial.print("Phone 2: ");
    //   send_sms("Nha dang co ke dot nhap. Goi 113 gap!!!", number2);
    // }
    if(number3 != ""){
      Serial.print("Phone 3: ");
      send_sms("Nha dang co ke dot nhap. Goi 113 gap!!!", number3);
    }
    // SendMessage_trom();
    mode_bao_dong = 7;
  }

  while (mode_bao_dong == 7){
    dong_gieng();
    // check_dung_motor();
    count_am_thanh_co_trom = 0;
    int giatriQuangtro = analogRead(analog_quangtro);
    int giatricambienmua = digitalRead(rain_sensor);
    //Serial.println(giatriQuangtro);
    float do_am = dht.readHumidity();
    float nhiet_do = dht.readTemperature();
    float f = dht.readTemperature(true);
    float hic = dht.computeHeatIndex(nhiet_do, do_am, false);
    float hif = dht.computeHeatIndex(f, do_am);
    // Serial.print(nhiet_do);
    // Serial.println(digitalRead(rain_sensor));
    // Serial.println(giatriQuangtro);
    song_am();
    WiFiClient client = wifiServer.available();
    if (client) {
      while (client.connected()) {
        int giatriQuangtro = analogRead(analog_quangtro);
        int giatricambienmua = digitalRead(rain_sensor);
        //Serial.println(giatriQuangtro);
        float do_am = dht.readHumidity();
        float nhiet_do = dht.readTemperature();
        float f = dht.readTemperature(true);
        float hic = dht.computeHeatIndex(nhiet_do, do_am, false);
        float hif = dht.computeHeatIndex(f, do_am);
        String string_nhiet_do = String(nhiet_do);
        String string_do_am = String(do_am);
        String string_quang_tro = String(giatriQuangtro);
        String string_cam_bien_mua = String(giatricambienmua);
        String string_cam_bien_song_am = String(distanceCm);
        stringTwo += stringOne;
        stringTwo += string_nhiet_do;
        stringTwo += ";";
        stringTwo += string_do_am;
        stringTwo += ";";
        stringTwo += string_quang_tro;
        stringTwo += ";";
        stringTwo += string_cam_bien_mua;
        stringTwo += ";";
        stringTwo += string_cam_bien_song_am;
        stringTwo += ";";
        Serial.println(stringTwo);
        client.print(stringTwo);
        stringOne = "";
        stringTwo = "";
        String c = client.readString();
        Serial.println(c);

        dong_gieng();

        // delay(500);
        if (c == "lua")
        {
          Serial.print("bao chay");
          mode_bao_dong = 1;
        }
        // if (c == ""){
        //   break;
        // }
      }
      client.stop();
      Serial.println("Client disconnected");
      }

  }
  
  while (mode_bao_dong == 1){
    Serial.print("gui dien thoai");
    // SendMessage();
    // call();
    make_multi_call();
    // for(int i = 0; i <3000;i++){
    //   Serial.print(i);
    // }
    
    delay(500);
    // delay(2000);
    mode_bao_dong = 2;
  }
  
  while (mode_bao_dong == 2){
    Serial.print("goi tin nhan");
    // call();
    // if(number1 != ""){
    //   Serial.print("Phone 1: ");
    //   send_sms("Nha dang chay. Goi 114 gap!!!", number1);
    // }
    // if(number2 != ""){
    //   Serial.print("Phone 2: ");
    //   send_sms("Nha dang chay. Goi 114 gap!!!", number2);
    // }
    if(number3 != ""){
      Serial.print("Phone 3: ");
      send_sms("Nha dang chay. Goi 114 gap!!!", number3);
    }
    // SendMessage();
    // for(int i = 0; i <3000;i++){
      
    //   Serial.print(i);
    // }
    // delay(500);
    // delay(2000);
    mode_bao_dong = 3;
  }

  while(mode_bao_dong == 3){
    Serial.print("che do bao chay");
    digitalWrite(Den_bao_dong, HIGH);
    analogWrite(Den_bao_chua_chay, 255);

    mo_gieng();
    // Serial.println("cua HIGH");
    myPlayer.play(5);
    for(int i = 0; i <30000;i++){
      Serial.print(i);
      mo_gieng();
      // delay(1000);
    }
  }
}
