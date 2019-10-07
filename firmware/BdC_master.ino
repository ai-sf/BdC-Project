//  ╔═════════════════════════════════════════════════════════════════════════════════╗
//  ║                                                                                 ║
//  ║                             bottaDiCoulomb_master                               ║
//  ║                                  version 1.15                                   ║
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

#define VERSION          "v1.15"

#define DEBUG_MODE       0

#define MESH_SSID        "mesh_ssid"
#define MESH_PASSWORD    "mesh_pass"
#define MESH_PORT     5555
#define MESH_CHANNEL    13
#define MESH_HIDDEN      1

#define LED_PIN         D4 //GPIO 2

painlessMesh mesh;
SimpleList<uint32_t> nodes;
String inputString;
bool stringComplete;

uint8_t luminosita=100;
unsigned long ledFlashStart;

bool offMode;

void checkSerialData()
{
  while(Serial.available())
  {
    char inChar=(char)Serial.read();
    inputString+=inChar;
    if(inChar=='\n')
      stringComplete=1;
  }
}

void setup()
{
  Serial.begin(115200);

  pinMode(LED_PIN,OUTPUT);

  mesh.init(MESH_SSID,MESH_PASSWORD,MESH_PORT,WIFI_AP_STA,MESH_CHANNEL,MESH_HIDDEN);
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);

  mesh.setRoot();
}

void loop()
{
  if(!offMode)
  {
    mesh.update();

    if(nodes.size()==0)
    {
      if(millis()%500<50)
        digitalWrite(LED_PIN,0);
      else
        digitalWrite(LED_PIN,1);
    }
    else if(millis()-ledFlashStart<200 && (millis()-ledFlashStart)%50<25)
      digitalWrite(LED_PIN,1);
    else
      digitalWrite(LED_PIN,0);

    checkSerialData();

    if(stringComplete)
    {
      if(inputString=="timeNow\n")
      {
        Serial.print("--- TIME NOW -----------------:");
        Serial.print("timeNow=");
        Serial.println(mesh.getNodeTime());
      }
      else if(inputString.startsWith("lum"))
      {
        uint8_t luminositaTemp=0;
        for(int i=0;i<3;i++)
        {
          luminositaTemp*=10;
          luminositaTemp+=inputString.substring(i+3,i+4).toInt();
        }
        if(luminositaTemp>=0 && luminositaTemp<=100)
        {
          luminosita=luminositaTemp;
          mesh.sendBroadcast(inputString);
          ledFlashStart=millis();
        }
      }
      else if(inputString=="off\n")
      {
          String offString="off";
          mesh.sendBroadcast(offString);
          ledFlashStart=millis();
          offMode=1;
      }
      else if(inputString=="ver\n")
      {
          Serial.print("--- VERSION ------------------:");
          Serial.print("master_version=");
          Serial.println(VERSION+String("_master"));
          String verString="ver";
          mesh.sendBroadcast(verString);
          ledFlashStart=millis();
      }
      else if(inputString.startsWith("send"))
      {
        uint32_t target=0;
        target=getValue(inputString,' ',1).toInt();

        String message=getValue(inputString,' ',2).substring(0,1);

        if(mesh.isConnected(target))
        {
          mesh.sendSingle(target,message);
          ledFlashStart=millis();

          Serial.print("--- MESSAGE SENT -------------:");
          Serial.print("to=");
          Serial.print(target);
          Serial.print(",msgText=");
          Serial.println(message);
        }
        else
        {
          Serial.print("--- MESSAGE ERROR ------------:");
          Serial.print("to=");
          Serial.print(target);
          Serial.println(",not connected!");
        }
      }
      else if(inputString.startsWith("upgrade"))
      {
        if(getValue(inputString,' ',4)=="" || getValue(inputString,' ',5)!="")
        {
          Serial.println("--- UPGRADE ERROR ------------:");
          Serial.println("4 arguments needed (target,ssid,pass,url)");
        }
        else
        {
          Serial.println("--- UPGRADE ------------------:");
          Serial.print("target=");
          Serial.println(getValue(inputString,' ',1));
          Serial.print("ssid=");
          Serial.println(getValue(inputString,' ',2));
          Serial.print("pass=");
          Serial.println(getValue(inputString,' ',3));
          Serial.print("url=");
          Serial.println(getValue(inputString,' ',4));
          mesh.sendBroadcast(inputString);
          ledFlashStart=millis();
        }
      }
      else if(inputString=="topo\n")
      {
        Serial.println("--- TOPOLOGY -----------------:");
        Serial.print("topology=");
        Serial.println(mesh.subConnectionJson());
      }
      else if(inputString=="restart\n")
      {
        Serial.print("--- RESTART ------------------:");
        String rstString="rst "+String(mesh.getNodeTime()+10000000);
        mesh.sendBroadcast(rstString);
        ledFlashStart=millis();
      }

      inputString="";
      stringComplete=0;
    }
  }
  else
  {
    while(1)
    {
      digitalWrite(LED_PIN,1);
      delay(250);
      digitalWrite(LED_PIN,0);
      delay(250);
    }
  }
}

void receivedCallback(uint32_t from,String &msg)
{
  Serial.print("--- MESSAGE RECEIVED ---------:");
  Serial.print("from=");
  Serial.print(from);
  Serial.print(",msgText=");
  Serial.println(msg.c_str());

  ledFlashStart=millis();
}

void newConnectionCallback(uint32_t nodeId)
{
  Serial.println("--- NEW CONNECTION -----------");
  masterIdentification();
  ledFlashStart=millis();
}

void changedConnectionCallback()
{
  Serial.println("--- CHANGED CONNECTION -------");
  masterIdentification();
  ledFlashStart=millis();
}

void nodeTimeAdjustedCallback(int32_t offset)
{
  #if DEBUG_MODE //-----------------------------------------------------------------#┐
  Serial.print("--- TIME ADJUSTED ------------:");
  Serial.print("time=");
  Serial.print(mesh.getNodeTime());
  Serial.print(",offset=");
  Serial.println(offset);
  #endif //-------------------------------------------------------------------------#┘

  ledFlashStart=millis();
}

void masterIdentification()
{
  if(!offMode)
  {
    Serial.print("--- MASTER IDENTIFICATION ----:");
    Serial.print("time=");
    Serial.print(mesh.getNodeTime());
    nodes=mesh.getNodeList();
    Serial.print(",nodes=");
    Serial.print(nodes.size());

    if(nodes.size()>0)
    {
      Serial.print(",list=");
      SimpleList<uint32_t>::iterator node=nodes.begin();
      while(node!=nodes.end())
      {
        if(node!=nodes.begin()) Serial.print("|");
        Serial.printf("%u", *node);
        node++;
      }

      String captain="I am the captain now";
      mesh.sendBroadcast(captain);

      String zeroLuminosita;
      if(luminosita<100)
        zeroLuminosita+="0";
      if(luminosita<10)
        zeroLuminosita+="0";
      zeroLuminosita+=luminosita;
      mesh.sendBroadcast("lum"+zeroLuminosita);

      ledFlashStart=millis();
    }
    Serial.println();
  }
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
