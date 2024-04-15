## sudo mknod /dev/ttyUSB0 c 188 0
## sudo chmod 777 /dev/ttyUSB0
"""
Il seguente codice emula un master del gioco.
Il codice va eseguito per ogni domanda dopo che parte il conto alla rovescia. Si esegue con:
python3 master.py /dev/pts/n; con n un qualche numero che viene stampato dal master;
Leggere nella Clasase Master nel main del gioco per vedere meglio questo dettaglio
La lista dei telecomandi va aggiornata a mano, non li legge dal file di configurazione
"""
import numpy as np
import serial, time, argparse


description='Codice per emulare il master'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('name_port',  help='nome della porta su cui scrivere')
args = parser.parse_args()

ser = serial.Serial(args.name_port, 115200, timeout=None)
print(ser.name) 

TEL = [977148330, 977144982, 977143789, 977143982, 977141870, 977148973, 977149543, 981430530, 977151320, 977149772]
ANS = ["A", "", "D", "", ""]


timenow_msg0 = f"--- TIME NOW -----------------:timeNow={time.time()}"
ser.write(timenow_msg0.encode())
time.sleep(1)

for tel in TEL:
    ans = ANS[np.random.randint(5)]
    score_msg = f"--- MESSAGE RECEIVED ---------:from={tel},msgText={ans},msgTime={time.time()}(,battery=100)"
    ser.write(score_msg.encode())
    time.sleep(1)

time.sleep(7)
timenow_msg1 = f"--- TIME NOW -----------------:timeNow={time.time()}"
ser.write(timenow_msg1.encode())

