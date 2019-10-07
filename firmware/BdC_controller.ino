//  ╔═════════════════════════════════════════════════════════════════════════════════╗
//  ║                                                                                 ║
//  ║                           bottaDiCoulomb_controller                             ║
//  ║                                  version 0.7                                    ║
//  ║                                                                                 ║
//  ║                            (C) 2018 Michele Pirola                              ║
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

#define VERSION                      "v0.7"

#define MESH_SSID                    "mesh_ssid"
#define MESH_PASSWORD                "mesh_pass"
#define MESH_PORT                 5555
#define MESH_CHANNEL                13
#define MESH_HIDDEN                  1

#define OFF_BUTTON_DELAY          1000

#define TIMEOUT_MESH_UPDATE_OFF  20000
#define TIMEOUT_TURN_OFF         60000
#define TIMEOUT_NO_CONNECT_OFF  300000

#define LED_PIN                     D4 //GPIO  2

#define PULS_RED_PIN                D0 //GPIO 16
#define PULS_GREEN_PIN              D1 //GPIO 14
#define PULS_YELLOW_PIN             D5 //GPIO  5
#define PULS_BLUE_PIN               D6 //GPIO 12
#define PULS_BLACK_PIN              D7 //GPIO 13
#define PULS_WHITE_PIN              D8 //GPIO 15

uint32_t master_id;
unsigned long millisAnswer;
bool answerReady=1;

unsigned long startAllButtonPressed;
unsigned long startOff;
unsigned long lastDisconnect;

bool ledFlashConnection=1;
bool ledFlashTurningOff;

painlessMesh mesh;

uint32_t timeRestart;

void setup()
{
  pinMode(LED_PIN, OUTPUT);

  pinMode(PULS_RED_PIN,INPUT);
  pinMode(PULS_YELLOW_PIN,INPUT);
  pinMode(PULS_GREEN_PIN,INPUT);
  pinMode(PULS_BLUE_PIN,INPUT);
  pinMode(PULS_BLACK_PIN,INPUT);
  pinMode(PULS_WHITE_PIN,INPUT);

  mesh.init(MESH_SSID,MESH_PASSWORD,MESH_PORT,WIFI_AP_STA,MESH_CHANNEL,MESH_HIDDEN);
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);

  mesh.setContainsRoot();
}

void loop()
{
  if(timeRestart>0 && mesh.getNodeTime()>timeRestart)
  {
    ESP.restart();
  }

  if((lastDisconnect==0 || millis()-lastDisconnect<TIMEOUT_NO_CONNECT_OFF) && (startOff==0 || millis()-startOff<TIMEOUT_MESH_UPDATE_OFF))
    mesh.update();

  if(ledFlashTurningOff)
  {
    if(millis()%500<250)
      digitalWrite(LED_PIN,0);
    else
      digitalWrite(LED_PIN,1);
  }
  else if(ledFlashConnection)
  {
    if(millis()%500<50)
      digitalWrite(LED_PIN,0);
    else
      digitalWrite(LED_PIN,1);
  }
  else if(millis()-millisAnswer<200)
  {
    if((millis()-millisAnswer)%50<25)
      digitalWrite(LED_PIN,0);
    else
      digitalWrite(LED_PIN,1);
  }
  else
    digitalWrite(LED_PIN,0);

  if(startOff==0 && lastDisconnect!=0 && millis()-lastDisconnect>TIMEOUT_NO_CONNECT_OFF)
    turnOff();

  if(master_id!=0 && mesh.isConnected(master_id) && answerReady)
  {
    if(digitalRead(PULS_RED_PIN) && !digitalRead(PULS_YELLOW_PIN) && !digitalRead(PULS_GREEN_PIN) && !digitalRead(PULS_BLUE_PIN) && !digitalRead(PULS_BLACK_PIN) && !digitalRead(PULS_WHITE_PIN))
    {
      String answer="RED,msgTime="+String(mesh.getNodeTime());
      mesh.sendSingle(master_id,answer);
      millisAnswer=millis();
      answerReady=0;
    }

    if(!digitalRead(PULS_RED_PIN) && digitalRead(PULS_YELLOW_PIN) && !digitalRead(PULS_GREEN_PIN) && !digitalRead(PULS_BLUE_PIN) && !digitalRead(PULS_BLACK_PIN) && !digitalRead(PULS_WHITE_PIN))
    {
      String answer="GREEN,msgTime="+String(mesh.getNodeTime());
      mesh.sendSingle(master_id,answer);
      millisAnswer=millis();
      answerReady=0;
    }

    if(!digitalRead(PULS_RED_PIN) && !digitalRead(PULS_YELLOW_PIN) && digitalRead(PULS_GREEN_PIN) && !digitalRead(PULS_BLUE_PIN) && !digitalRead(PULS_BLACK_PIN) && !digitalRead(PULS_WHITE_PIN))
    {
      String answer="YELLOW,msgTime="+String(mesh.getNodeTime());
      mesh.sendSingle(master_id,answer);
      millisAnswer=millis();
      answerReady=0;
    }

    if(!digitalRead(PULS_RED_PIN) && !digitalRead(PULS_YELLOW_PIN) && !digitalRead(PULS_GREEN_PIN) && digitalRead(PULS_BLUE_PIN) && !digitalRead(PULS_BLACK_PIN) && !digitalRead(PULS_WHITE_PIN))
    {
      String answer="BLUE,msgTime="+String(mesh.getNodeTime());
      mesh.sendSingle(master_id,answer);
      millisAnswer=millis();
      answerReady=0;
    }

    if(!digitalRead(PULS_RED_PIN) && !digitalRead(PULS_YELLOW_PIN) && !digitalRead(PULS_GREEN_PIN) && !digitalRead(PULS_BLUE_PIN) && digitalRead(PULS_BLACK_PIN) && !digitalRead(PULS_WHITE_PIN))
    {
      String answer="BLACK,msgTime="+String(mesh.getNodeTime());
      mesh.sendSingle(master_id,answer);
      millisAnswer=millis();
      answerReady=0;
    }

    if(!digitalRead(PULS_RED_PIN) && !digitalRead(PULS_YELLOW_PIN) && !digitalRead(PULS_GREEN_PIN) && !digitalRead(PULS_BLUE_PIN) && !digitalRead(PULS_BLACK_PIN) && digitalRead(PULS_WHITE_PIN))
    {
      String answer="WHITE,msgTime="+String(mesh.getNodeTime());
      mesh.sendSingle(master_id,answer);
      millisAnswer=millis();
      answerReady=0;
    }

    startAllButtonPressed=0;
  }
  else
  {
    if(digitalRead(PULS_RED_PIN) && digitalRead(PULS_YELLOW_PIN) && digitalRead(PULS_GREEN_PIN) && digitalRead(PULS_BLUE_PIN) && digitalRead(PULS_BLACK_PIN) && digitalRead(PULS_WHITE_PIN))
    {
      if(startAllButtonPressed==0)
        startAllButtonPressed=millis();
      else if(millis()-startAllButtonPressed>=OFF_BUTTON_DELAY)
        turnOff();
    }
    else
      startAllButtonPressed=0;
  }

  if(millis()-millisAnswer>250)
    answerReady=1;

  if(master_id!=0 && mesh.isConnected(master_id))
  {
    if(startOff==0)
      ledFlashConnection=0;
    else
    {
      ledFlashTurningOff=1;
    }

    if(lastDisconnect!=0 && startOff==0)
      lastDisconnect=0;
  }
  else
  {
    ledFlashConnection=1;

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
  if(msg=="I am the captain now" && master_id==0)
  {
    master_id=from;

    ledFlashConnection=0;

    if(lastDisconnect!=0)
      lastDisconnect=0;
  }
  else if(msg=="off")
  {
    startOff=millis();
  }
  else if(msg=="ver")
  {
    String version=VERSION+String("_controller");
    mesh.sendSingle(master_id,version);
  }
  else if(msg.startsWith("rst"))
  {
    timeRestart=strtoul(getValue(msg,' ',1).c_str(),NULL,10);
  }
  else if(msg.startsWith("upgrade") && (getValue(msg,' ',1)=="controller" || strtoul(getValue(msg,' ',1).c_str(), NULL, 10)==mesh.getNodeId()))
  {
    msg.remove(msg.length()-1);
    upgradeFW(getValue(msg,' ',2),getValue(msg,' ',3),getValue(msg,' ',4));
  }
}

void newConnectionCallback(uint32_t nodeId)
{
}

void changedConnectionCallback()
{
}

void nodeTimeAdjustedCallback(int32_t offset)
{
}

void turnOff()
{
  mesh.stop();
  delay(1000);
  ESP.deepSleep(0);
}

void upgradeFW(String ssid,String password,String url)
{
  unsigned long updateMillis=millis();

  while(millis()-updateMillis<5000)
    mesh.update();

  mesh.stop();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(),password.c_str());
  while(WiFi.status()!=WL_CONNECTED)
    delay(500);

  ESPhttpUpdate.rebootOnUpdate(1);
  t_httpUpdate_return ret=ESPhttpUpdate.update(url);
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
