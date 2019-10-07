//  ╔═════════════════════════════════════════════════════════════════════════════════╗
//  ║                                                                                 ║
//  ║                              bottaDiCoulomb_slave                               ║
//  ║                                  version 1.19                                   ║
//  ║                                                                                 ║
//  ║                            (C) 2019 Michele Pirola                              ║
//  ║                                                                                 ║
//  ╠═════════════════════════════════════════════════════════════════════════════════╣
//  ║                                                                                 ║
//  ║      This program is free software; you can redistribute it and/or modify       ║
//  ║      it under the terms of the GNU General Public License as published by       ║
//  ║       the Free Software Foundation; either version 3 of the License, or         ║
//  ║                      (at your option) any later version.                        ║
//  ║                                                                                 ║
//  ║         This program is distributed in the hope that it will be useful,         ║
//  ║         but WITHOUT ANY WARRANTY; without even the implied warranty of          ║
//  ║          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           ║
//  ║                  GNU General Public License for more details.                   ║
//  ║                                                                                 ║
//  ║        You should have received a copy of the GNU General Public License        ║
//  ║     along with this program; if not, write to the Free Software Foundation,     ║
//  ║        Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA        ║
//  ║                                                                                 ║
//  ╚═════════════════════════════════════════════════════════════════════════════════╝

#include <painlessMesh.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266httpUpdate.h>

#define VERSION                      "v1.19"

#define SOUND_ENABLED                1
#define RGBLED_ENABLED               1
#define SERIALDEBUG_ENABLED          0

#define MESH_SSID                    "mesh_ssid"
#define MESH_PASSWORD                "mesh_pass"
#define MESH_PORT                 5555
#define MESH_CHANNEL                13
#define MESH_HIDDEN                  1

#define NUMBER_FLASH_RESULT         40
#define PERIOD_FLASH_RESULT        150

#define FREQ_SOUND_ON_1            660
#define FREQ_SOUND_ON_2            770
#define FREQ_SOUND_ANSWER         1100
#define FREQ_SOUND_CONNECTED       990
#define FREQ_SOUND_DISCONNECTED    220
#define FREQ_SOUND_UPGRADE        2000

#define OFF_BUTTON_DELAY          1000

#define TIMEOUT_MESH_UPDATE_OFF  20000
#define TIMEOUT_TURN_OFF         60000
#define TIMEOUT_NO_CONNECT_OFF  300000

#define LED_PIN                     D4 //GPIO  2
#define BUZ_PIN                     D8 //GPIO 15

#define PULS_A_PIN                  D1 //GPIO  5
#define PULS_B_PIN                  D0 //GPIO 16
#define PULS_C_PIN                  D5 //GPIO 14
#define PULS_D_PIN                  D6 //GPIO 12
#define PULS_E_PIN                  D7 //GPIO 13

#if RGBLED_ENABLED //-------------------------------------------------------------#┐
#include <NeoPixelBrightnessBus.h>
#define APA_PIN                     D2 //GPIO  4
#endif //-------------------------------------------------------------------------#┘

uint32_t master_id;
unsigned long millisAnswer;
bool answerReady=1;

unsigned long startFlash;
uint8_t i;
bool led_off;
char answerType;

unsigned long startAllButtonPressed;
unsigned long startOff;
unsigned long lastDisconnect;

painlessMesh mesh;

uint32_t timeRestart;

#if RGBLED_ENABLED //-------------------------------------------------------------#┐
NeoPixelBrightnessBus<NeoRgbFeature, NeoEsp8266BitBang800KbpsMethod> apaBus(1,APA_PIN);
RgbColor off    (  0,  0,  0);
RgbColor red    (255,  0,  0);
RgbColor green  (  0,255,  0);
RgbColor blue   (  0,  0,255);
RgbColor yellow (255,180,  0);
RgbColor orange (255, 60,  0);
RgbColor magenta(255,  0,200);
RgbColor white  (255,255,255);
#endif //-------------------------------------------------------------------------#┘

#if SOUND_ENABLED //--------------------------------------------------------------#┐
bool disconnectSound;
#endif //-------------------------------------------------------------------------#┘

void setup()
{
  #if SERIALDEBUG_ENABLED //--------------------------------------------------------#┐
  Serial.begin(115200);
  #endif //-------------------------------------------------------------------------#┘

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZ_PIN, OUTPUT);

  pinMode(PULS_A_PIN,INPUT);
  pinMode(PULS_B_PIN,INPUT);
  pinMode(PULS_C_PIN,INPUT);
  pinMode(PULS_D_PIN,INPUT);
  pinMode(PULS_E_PIN,INPUT);

  digitalWrite(LED_PIN,1);

  #if RGBLED_ENABLED //-------------------------------------------------------------#┐
  apaBus.Begin();
  apaBus.Show();
  #endif //-------------------------------------------------------------------------#┘

  #if SERIALDEBUG_ENABLED //--------------------------------------------------------#┐
  mesh.setDebugMsgTypes(ERROR | STARTUP | MESH_STATUS | CONNECTION | SYNC | S_TIME | COMMUNICATION | GENERAL | MSG_TYPES | REMOTE | APPLICATION | DEBUG);
  #endif //-------------------------------------------------------------------------#┘

  mesh.init(MESH_SSID,MESH_PASSWORD,MESH_PORT,WIFI_AP_STA,MESH_CHANNEL,MESH_HIDDEN);
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);

  mesh.setContainsRoot();

  #if SOUND_ENABLED //--------------------------------------------------------------#┐
  tone(BUZ_PIN, FREQ_SOUND_ON_1, 200);
  delay(200);
  tone(BUZ_PIN, FREQ_SOUND_ON_2, 200);
  #endif //-------------------------------------------------------------------------#┘
}

void loop()
{
  if(timeRestart>0 && mesh.getNodeTime()>timeRestart)
  {
    ESP.restart();
  }

  if((lastDisconnect==0 || millis()-lastDisconnect<TIMEOUT_NO_CONNECT_OFF) && (startOff==0 || millis()-startOff<TIMEOUT_MESH_UPDATE_OFF))
    mesh.update();

  if(startOff==0 && lastDisconnect!=0 && millis()-lastDisconnect>TIMEOUT_NO_CONNECT_OFF)
    turnOff();

  if(master_id!=0 && mesh.isConnected(master_id))
  {
    if(answerReady)
    {
      if(digitalRead(PULS_A_PIN) && !digitalRead(PULS_B_PIN) && !digitalRead(PULS_C_PIN) && !digitalRead(PULS_D_PIN) && !digitalRead(PULS_E_PIN))
      {
        #if SOUND_ENABLED //--------------------------------------------------------------#┐
        tone(BUZ_PIN, FREQ_SOUND_ANSWER, 200);
        #endif //-------------------------------------------------------------------------#┘

        String answer="A,msgTime="+String(mesh.getNodeTime());
        mesh.sendSingle(master_id,answer);
        millisAnswer=millis();
        answerReady=0;
      }

      if(!digitalRead(PULS_A_PIN) && digitalRead(PULS_B_PIN) && !digitalRead(PULS_C_PIN) && !digitalRead(PULS_D_PIN) && !digitalRead(PULS_E_PIN))
      {
        #if SOUND_ENABLED //--------------------------------------------------------------#┐
        tone(BUZ_PIN, FREQ_SOUND_ANSWER, 200);
        #endif //-------------------------------------------------------------------------#┘

        String answer="B,msgTime="+String(mesh.getNodeTime());
        mesh.sendSingle(master_id,answer);
        millisAnswer=millis();
        answerReady=0;
      }

      if(!digitalRead(PULS_A_PIN) && !digitalRead(PULS_B_PIN) && digitalRead(PULS_C_PIN) && !digitalRead(PULS_D_PIN) && !digitalRead(PULS_E_PIN))
      {
        #if SOUND_ENABLED //--------------------------------------------------------------#┐
        tone(BUZ_PIN, FREQ_SOUND_ANSWER, 200);
        #endif //-------------------------------------------------------------------------#┘

        String answer="C,msgTime="+String(mesh.getNodeTime());
        mesh.sendSingle(master_id,answer);
        millisAnswer=millis();
        answerReady=0;
      }

      if(!digitalRead(PULS_A_PIN) && !digitalRead(PULS_B_PIN) && !digitalRead(PULS_C_PIN) && digitalRead(PULS_D_PIN) && !digitalRead(PULS_E_PIN))
      {
        #if SOUND_ENABLED //--------------------------------------------------------------#┐
        tone(BUZ_PIN, FREQ_SOUND_ANSWER, 200);
        #endif //-------------------------------------------------------------------------#┘

        String answer="D,msgTime="+String(mesh.getNodeTime());
        mesh.sendSingle(master_id,answer);
        millisAnswer=millis();
        answerReady=0;
      }

      if(!digitalRead(PULS_A_PIN) && !digitalRead(PULS_B_PIN) && !digitalRead(PULS_C_PIN) && !digitalRead(PULS_D_PIN) && digitalRead(PULS_E_PIN))
      {
        #if SOUND_ENABLED //--------------------------------------------------------------#┐
        tone(BUZ_PIN, FREQ_SOUND_ANSWER, 200);
        #endif //-------------------------------------------------------------------------#┘

        String answer="E,msgTime="+String(mesh.getNodeTime());
        mesh.sendSingle(master_id,answer);
        millisAnswer=millis();
        answerReady=0;
      }

      startAllButtonPressed=0;
    }
  }
  else
  {
    if(digitalRead(PULS_A_PIN) && digitalRead(PULS_B_PIN) && digitalRead(PULS_C_PIN) && digitalRead(PULS_D_PIN) && digitalRead(PULS_E_PIN))
    {
      if(startAllButtonPressed==0)
        startAllButtonPressed=millis();
      else if(millis()-startAllButtonPressed>=OFF_BUTTON_DELAY)
        turnOff();
    }
    else
      startAllButtonPressed=0;
  }

  if(millis()-millisAnswer<1000 && master_id!=0)
  {
    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    apaBus.SetPixelColor(0, magenta);
    apaBus.Show();
    #endif //-------------------------------------------------------------------------#┘
  }
  else if(!digitalRead(PULS_A_PIN) && !digitalRead(PULS_B_PIN) && !digitalRead(PULS_C_PIN) && !digitalRead(PULS_D_PIN) && !digitalRead(PULS_E_PIN))
    answerReady=1;

  if(answerType=='R')
  {
    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    if(startFlash==0)
    {
      startFlash=millis();
      led_off=0;
      i=0;
    }

    if(i<NUMBER_FLASH_RESULT)
    {
      if((millis()-startFlash)%PERIOD_FLASH_RESULT<(PERIOD_FLASH_RESULT/2))
      {
        apaBus.SetPixelColor(0, green);
        apaBus.Show();
        led_off=0;
      }
      else
      {
        apaBus.SetPixelColor(0, 0);
        apaBus.Show();
        if(!led_off) i++;
        led_off=1;
      }
    }
    else
    {
      startFlash=0;
      answerType='\0';
    }
    #endif //-------------------------------------------------------------------------#┘
  }
  else if(answerType=='A')
  {
    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    if(startFlash==0)
    {
      startFlash=millis();
      led_off=0;
      i=0;
    }

    if(i<NUMBER_FLASH_RESULT)
    {
      if((millis()-startFlash)%PERIOD_FLASH_RESULT<(PERIOD_FLASH_RESULT/2))
      {
        apaBus.SetPixelColor(0, yellow);
        apaBus.Show();
        led_off=0;
      }
      else
      {
        apaBus.SetPixelColor(0, 0);
        apaBus.Show();
        if(!led_off) i++;
        led_off=1;
      }
    }
    else
    {
      startFlash=0;
      answerType='\0';
    }
    #endif //-------------------------------------------------------------------------#┘
  }
  else if(answerType=='W')
  {
    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    if(startFlash==0)
    {
      startFlash=millis();
      led_off=0;
      i=0;
    }

    if(i<NUMBER_FLASH_RESULT)
    {
      if((millis()-startFlash)%PERIOD_FLASH_RESULT<(PERIOD_FLASH_RESULT/2))
      {
        apaBus.SetPixelColor(0, red);
        apaBus.Show();
        led_off=0;
      }
      else
      {
        apaBus.SetPixelColor(0, 0);
        apaBus.Show();
        if(!led_off) i++;
        led_off=1;
      }
    }
    else
    {
      startFlash=0;
      answerType='\0';
    }
    #endif //-------------------------------------------------------------------------#┘
  }
  else if(master_id!=0 && mesh.isConnected(master_id))
  {
    #if SOUND_ENABLED //--------------------------------------------------------------#┐
    if(!disconnectSound)
    {
      tone(BUZ_PIN, FREQ_SOUND_CONNECTED, 200);
      disconnectSound=1;
    }
    #endif //-------------------------------------------------------------------------#┘

    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    if(startOff==0)
    {
      if(answerReady)
        apaBus.SetPixelColor(0, blue);
    }
    else
    {
      if((millis()-startOff)%500<250)
        apaBus.SetPixelColor(0, orange);
      else
        apaBus.SetPixelColor(0, blue);
    }
    apaBus.Show();
    #endif //-------------------------------------------------------------------------#┘

    if(lastDisconnect!=0 && startOff==0)
      lastDisconnect=0;
  }
  else
  {
    #if SOUND_ENABLED //--------------------------------------------------------------#┐
    if(disconnectSound)
    {
      tone(BUZ_PIN, FREQ_SOUND_DISCONNECTED, 200);
      disconnectSound=0;
    }
    #endif //-------------------------------------------------------------------------#┘

    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    apaBus.SetPixelColor(0, orange);
    apaBus.Show();
    #endif //-------------------------------------------------------------------------#┘

    if(lastDisconnect==0)
      lastDisconnect=millis();
  }

  if(startOff>0 && millis()-startOff>TIMEOUT_TURN_OFF)
  {
    turnOff();
  }
}

void receivedCallback(uint32_t from, String &msg)
{
  #if SERIALDEBUG_ENABLED //--------------------------------------------------------#┐
  Serial.printf("Received from %u msg=%s\n", from, msg.c_str());
  #endif //-------------------------------------------------------------------------#┘

  if(msg=="I am the captain now" && master_id==0)
  {
    master_id=from;

    #if SOUND_ENABLED //--------------------------------------------------------------#┐
    if(!disconnectSound)
    {
      tone(BUZ_PIN, FREQ_SOUND_CONNECTED, 200);
      disconnectSound=1;
    }
    #endif //-------------------------------------------------------------------------#┘

    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    apaBus.SetPixelColor(0, blue);
    apaBus.Show();
    #endif //-------------------------------------------------------------------------#┘

    if(lastDisconnect!=0)
      lastDisconnect=0;
  }
  else if(msg.startsWith("lum"))
  {
    uint8_t luminosita=0;
    for(int i=0;i<3;i++)
    {
      luminosita*=10;
      luminosita+=msg.substring(i+3,i+4).toInt();
    }
    if(luminosita>=0 && luminosita<=100)
      apaBus.SetBrightness(luminosita*255/100.);
  }
  else if(msg=="off")
  {
    startOff=millis();
  }
  else if(msg=="ver")
  {
    String version=VERSION+String("_slave");
    mesh.sendSingle(master_id,version);
  }
  else if(msg.startsWith("rst"))
  {
    timeRestart=strtoul(getValue(msg,' ',1).c_str(),NULL,10);
  }
  else if(msg.startsWith("upgrade") && (getValue(msg,' ',1)=="slave") || strtoul(getValue(msg,' ',1).c_str(), NULL, 10)==mesh.getNodeId())
  {
    msg.remove(msg.length()-1);
    upgradeFW(getValue(msg,' ',2),getValue(msg,' ',3),getValue(msg,' ',4));
  }
  else if(msg=="R" && from==master_id)
    answerType='R';
  else if(msg=="A" && from==master_id)
    answerType='A';
  else if(msg=="W" && from==master_id)
    answerType='W';
}

void newConnectionCallback(uint32_t nodeId)  //nuovo membro connesso
{
}

void changedConnectionCallback()
{
}

void nodeTimeAdjustedCallback(int32_t offset)
{
  #if SERIALDEBUG_ENABLED //--------------------------------------------------------#┐
  Serial.printf("Adjusted time %u. Offset = %d\n", mesh.getNodeTime(), offset);
  #endif //-------------------------------------------------------------------------#┘
}

void turnOff()
{
  apaBus.SetPixelColor(0,off);
  apaBus.Show();
  mesh.stop();
  delay(1000);
  ESP.deepSleep(0);
}

void upgradeFW(String ssid,String password,String url)
{
  unsigned long updateMillis=millis();

  #if RGBLED_ENABLED //-------------------------------------------------------------#┐
  apaBus.SetPixelColor(0, white);
  apaBus.Show();
  #endif //-------------------------------------------------------------------------#┘

  #if SOUND_ENABLED //--------------------------------------------------------------#┐
  tone(BUZ_PIN, FREQ_SOUND_UPGRADE, 200);
  #endif //-------------------------------------------------------------------------#┘

  while(millis()-updateMillis<5000)
    mesh.update();

  mesh.stop();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(),password.c_str());
  while(WiFi.status()!=WL_CONNECTED)
    delay(500);

  ESPhttpUpdate.rebootOnUpdate(0);
  t_httpUpdate_return ret=ESPhttpUpdate.update(url);

  if(ret==HTTP_UPDATE_OK)
  {
    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    apaBus.SetPixelColor(0, green);
    apaBus.Show();
    delay(1000);
    #endif //-------------------------------------------------------------------------#┘
  }
  else
  {
    #if RGBLED_ENABLED //-------------------------------------------------------------#┐
    apaBus.SetPixelColor(0, red);
    apaBus.Show();
    delay(1000);
    #endif //-------------------------------------------------------------------------#┘
  }
  ESP.restart();
}

String getValue(String data,char separator,int index)
{
  int found=0;
  int strIndex[]={0,-1};
  int maxIndex=data.length()-1;

  for(int i=0;i<=maxIndex && found<=index;i++)
  {
    if(data.charAt(i)==separator || i==maxIndex)
    {
      found++;
      strIndex[0]=strIndex[1]+1;
      strIndex[1]=(i==maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0],strIndex[1]) : "";
}
