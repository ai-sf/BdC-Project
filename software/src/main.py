'''
BOTTA DI COULOMB

AISF (Associazione Italiana Studenti di Fisica)
Comitato Locale di Pavia

Github Repo: http://github.com/

######################################################################
############################ ATTENZIONE ##############################
######################################################################
##   SE SI PASSA DALL'EMULATORE AL TELECOMANDO VERO VANNO FATTI I   ##
##                 SEGUENTI CAMBIAMENTI AL CODICE:                  ##
##                                                                  ##
## 1) CAMBIARE IL NOME DELLA PORTA SUL FILE CHE DATE IN INPUT       ##
##                                                                  ##
## 2) MODIFICARE LE RIGHE PER LA LETTURA DELLA PORTA SERIALE        ##
##    NELLO SPECIFICO (nell'__init__ del Master):                   ##
##                                                                  ##
##    A) PER IL TELECOMANDO VERO USARE LE RIGHE:                    ##
##       print(port_name)                                           ##
##       self.ser = serial.Serial(port_name, 115200, timeout=None)  ##
##                                                                  ##
##    B) PER L'EMULATORE USARE LE RIGHE:                            ##
##       import os, pty, serial                                     ##
##       self.mastr, slave = pty.openpty()                          ##
##       s_name = os.ttyname(slave)                                 ##
##       self.ser = serial.Serial(s_name, 115200, timeout=None)     ##
##                                                                  ##
## 3) MODIFICARE LE RIGHE PER IL CONFRONTO DELLE STRINGHE           ##
##    NELLO SPECIFICO (in readserial di BDCApp):                    ##
##                                                                  ##
##    A) PER IL TELECOMANDO VERO USARE LE RIGHE:                    ##
##       tmp = self.master.ser.readline()                           ##
##       tmp = tmp.decode()                                         ##
##                                                                  ##
##    B) PER L'EMULATORE USARE LA RIGA:                             ##
##       tmp = self.master.risp()                                   ##
##                                                                  ##
## 4) MODIFICARE IL CALCOLO DEL PUNTEGGIO PER LA MISURA DEI TEMPI   ##
##    IN software/src/utils/calculate_score.py :                    ##
##                                                                  ##
##    A) PER IL TELECOMANDO VERO USARE LA RIGHA:                    ##
##       dt = (key - start_time)*pow(10,-6)                         ##
##                                                                  ##
##    B) PER L'EMULATORE USARE LA RIGA:                             ##
##       dt = (key - start_time)                                    ##
##                                                                  ##
######################################################################
######################################################################



'''

__version__ = '2.0.0'

import serial
import json
import os, sys, time

# Variabili per il percorso per i file multimediali e le icone
script_path = os.path.dirname(os.path.realpath(__file__))
os.environ['KIVY_WINDOW'] = 'sdl2'
# prevent Kivy from showing log messages
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

music_path = script_path + '/music/'
img_path   = script_path + '/img/'
icons_path = script_path + '/volti_fisici/'

# add module path for screen
module_path = script_path + '/uix/'
sys.path.insert(0, module_path)

# import App this is the main Class that manages UI's event loop
from kivy.app import App
from kivy.properties import NumericProperty, ListProperty, DictProperty, OptionProperty, StringProperty

#disable red point which appears with dx touch
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', 1) # 1 to close the window with esc, 0 to disable
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 160)
Config.set('graphics', 'top',  480)

#load icon font
import iconfonts.iconfonts as iconfonts
# Biologia
iconfonts.register('fa-leaf', script_path+'/iconfonts/fontawesome-webfont.ttf', script_path+'/iconfonts/font-awesome.fontd')
# Medicina
iconfonts.register('fa-heartbeat', script_path+'/iconfonts/fontawesome-webfont.ttf', script_path+'/iconfonts/font-awesome.fontd')
# Nutrizione
iconfonts.register('fa-cutlery', script_path+'/iconfonts/fontawesome-webfont.ttf', script_path+'/iconfonts/font-awesome.fontd')
# Chimica
iconfonts.register('fa-flask', script_path+'/iconfonts/fontawesome-webfont.ttf', script_path+'/iconfonts/font-awesome.fontd')
# Fisica
iconfonts.register('fa-magnet', script_path+'/iconfonts/fontawesome-webfont.ttf', script_path+'/iconfonts/font-awesome.fontd')
# Tecnologia
iconfonts.register('fa-cogs', script_path+'/iconfonts/fontawesome-webfont.ttf', script_path+'/iconfonts/font-awesome.fontd')


class Master:
    ''' Classe per gestire la comunicazione con il master
    '''

    def __init__(self, port_name):
        ''' Iniazializzazione della connessione
        '''
        try:
            # DA USARE CON IL MASTER
            #print(port_name)
            #self.ser = serial.Serial(port_name, 115200, timeout=None) # questo era per /dev/ttyUSB0
            
            # DA USARE CON L'EMULATORE
            #Tutto il seguente è per emulare il master
            import os, pty, serial
            self.mastr, slave = pty.openpty()
            s_name = os.ttyname(slave)
            #print(self.mastr, slave, s_name)
            self.ser = serial.Serial(s_name, 115200, timeout=None)
            print(self.ser.name) # va messa come imput al codice che emula il master del tipo:
            # python3 emulate_master/master.py self.ser.name 
            # Il codice che emula va eseguito per ogni domanda dopo che parte il conto alla rovescia
            # self.ser.name sarà qualcosa di parente di /dev/pts/n, con n un qualche numero intero
            
        except Exception as e:
            print("Connection to serial port failed"+f" error message: \n {str(e)}")
            exit()
    
    def risp(self):
        """ Per leggere da porta seriale dove l'emulatore scrive
        """
        answer = os.read(self.mastr, 1000)
        answer = str(answer)[1:]
        answer = answer[1:-1]
        return answer

    def write(self, string):
        ''' Scrittura sulla porta seriale
        '''
        #self.ser.write(string)
        self.ser.write(string.encode())

    def cleanup(self):
        ''' Chiusura della connessione
        '''
        self.ser.close()

class BDCApp(App):
    ''' Classe per il gioco vero e proprio
    '''

    # Attributi vari della classe

    dictANS = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5} # corrispondenza con il telecomando

    end_score  = False
    score_seen = False
    score_new  = False
    new_backup = False

    score_qst_ready = False
    score_gen_ready = False
    qst_done        = False

    serial_message = ''

    icons_path  = script_path + '/volti_fisici/'

    QST_DSP_CNT = StringProperty()
    QST_TOT_CNT = NumericProperty(0)
    QST_PAR_CNT = NumericProperty(0)
    QST_NOR_CNT = NumericProperty(0)
    QUESTIONS   = []

    SEC_CNT  = NumericProperty(0)
    SECTIONS = []

    HISTORY = []

    BATTERY_STATUS = {}

    ABSTENTIONS = {}
    # dictionary: { id :  score, ... }
    GENERAL_SCORE = {}
    # list of dictionary: [ { id : [score, time], ... } ...] with len(list) = number of questions
    QUESTION_SCORE = []
    # dictionary of dictionary: { section : { id : score, ... } ...} with len(list) = number of sections
    SECTION_SCORE = {}
    # dictionary of list { id : [answer to qst 1, answer to qst 2, ...] }
    # 'None' means abstention
    ANSWERS_GIVEN = []

    # dictionary: { id_winner: [list of section_icon(s)] }
    WINNER_OF_SECTIONS = {}

    SCT_FIRST_NAMES = []

    saved_ans = {}
    times     = []

    start_time     = None
    stop_time      = None
    startTimeGiven = False

    topologyRead = False

    stringa = u"\U0001F389"

    main_path = os.path.dirname(os.path.realpath(__file__))

    PRIZE = 300

    def build(self):
        ''' Costruzione dell'interfaccia utente
        '''

        import argparse
        description = 'Gioco botta di coulomb'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('config_file', help='path of the file with the input parameters')
        args = parser.parse_args()

        from utils.user import setGlobal
        setGlobal(args.config_file)

        self.BATTERY_STATUS = dict(zip(self.dictIDName.keys(),[-1]*len(self.dictIDName.keys())))
        self.ABSTENTIONS    = dict(zip(self.dictIDName.keys(),[0]*len(self.dictIDName.keys())))
        self.GENERAL_SCORE  = self.dictIDBonus

        self.last_question_backup = False

        self.RisposteDateList = [[0,0,0,0,0]]*self.starting_counter
        self.RisposteOK       = [0] * self.NUMERO_GIOCATORI

        if self.BACKUP:
            with open(self.filepath+'/backup.dat','r') as f:
                bckcontent = f.read()
                bcklist   = json.loads(bckcontent)
                print("---------Using backup!!------------")
                self.QST_DSP_CNT        = bcklist[0]
                self.QST_NOR_CNT        = bcklist[1]
                self.QST_TOT_CNT        = bcklist[2]
                self.QST_PAR_CNT        = bcklist[3]
                self.SEC_CNT            = bcklist[4]
                self.HISTORY            = bcklist[5]
                self.ABSTENTIONS        = bcklist[6]
                self.GENERAL_SCORE      = bcklist[7]
                self.QUESTION_SCORE     = bcklist[8]
                self.SECTION_SCORE      = bcklist[9]
                self.ANSWERS_GIVEN      = bcklist[10]
                self.WINNER_OF_SECTIONS = bcklist[11]
                self.SCT_FIRST_NAMES    = bcklist[12]
                self.score_new          = bcklist[13]
                self.new_backup         = True

            if self.SEC_CNT == len(self.SECTIONS):
                self.last_question_backup = True
                self.sorted_x = bcklist[14]
                self.SEC_CNT -= 1


        #music
        from kivy.core.audio import SoundLoader
        self.dance = SoundLoader.load(music_path+'bensound-dance.wav')
        self.dance.volume = 0.5
        self.dance.loop = True
        self.dance.play()

        self.timer_slow = SoundLoader.load(music_path+'timer_slow.wav')
        self.timer_slow.loop = False
        self.timer_fast = SoundLoader.load(music_path+'timer_fast.wav')
        self.timer_fast.loop = False
        self.timer_gong = SoundLoader.load(music_path+'timer_gong.wav')
        self.timer_gong.loop = False

        self.scifi = SoundLoader.load(music_path+'bensound-scifi.wav')
        self.scifi.volume = 0.5
        self.scifi.loop = True

        from utils.internalshell import internalShell
        self.shell = internalShell()

        # Inizializzazione del master per la comunicazione seriale
        if not self.no_serial:
            self.master = Master(self.port_name)
            import threading
            t = threading.Thread(target=self.readserial)
            t.daemon = True
            t.start()

        from uix.screenmanager import BDCScreenManager
        sm = BDCScreenManager()
        return sm

    def cmd_line_start(self):
        self.shell.cmdloop("type commands")

    def checkForTimeNow(self):
        '''
        Controlla periodicamente se l'ora attuale è stata
        ricevuta dall'interfaccia seriale e invia
        una richiesta di tempo se necessario.
        '''
        time.sleep(0.05)                        # Attendi per evitare sovraccarico
        if self.start_time is None:             # Se l'orario di inizio non è ancora stato ricevuto
            if self.no_serial is False:         # Se non è in modalità senza seriale
                self.master.write('timeNow\n')  # Richiedi l'orario corrente tramite
                                                # la comunicazione seriale

    def readserial(self):
        ''' Legge i messaggi ricevuti dalla porta seriale e gestisce le azioni corrispondenti
        '''

        import re
        # Definizione dei modelli di espressioni regolari per i messaggi attesi
        showman_msg  = r"--- MESSAGE RECEIVED ---------:from=2131961277,msgText=(\w+),msgTime=\d+"
        score_msg    = r"--- MESSAGE RECEIVED ---------:from=(\d{9}),msgText=([ABCDE]),msgTime=(\d+)(,battery=(-?\d+))?"
        timenow_msg  = r"--- TIME NOW -----------------:timeNow=(\d+)"
        topology_msg = r"topology=(.+)"

        # Loop infinito (fino a che non si termina inl gioco)
        while True:
            if self.no_serial is False:
                # QUESTA RIGA È PER L'EMULATORE
                tmp = self.master.risp()
                # QUESTE DUE SONO INVECE PER IL MASTER
                #tmp = self.master.ser.readline()
                #tmp = tmp.decode()
            else:
                tmp = "Bella zio!"
                
            letter = re.match(showman_msg, tmp)
            if letter:
                letter = letter.group(1)   # Estrae il comando dal messaggio
                print("Showman:"), letter  # Stampa il comando dello showman

               # Esegue l'azione corrispondente al comando
                if letter == "GREEN":
                    if hasattr(self.current_screen(), "next_button"):
                        if not self.current_screen().next_button.disabled:
                            self.current_screen().next_button.trigger_action(0)

                if letter == "RED":
                    if hasattr(self.current_screen(), "back_button"):
                        if not self.current_screen().back_button.disabled:
                            self.current_screen().back_button.trigger_action(0)

                if letter == "YELLOW":
                    if hasattr(self.current_screen(), "jolly_button"):
                        if not self.current_screen().jolly_button.disabled:
                            self.current_screen().jolly_button.trigger_action(0)

                if letter == "BLUE":
                    if hasattr(self.current_screen(), "timer_button"):
                        if not self.current_screen().timer_button.disabled:
                            self.current_screen().timer_button.trigger_action(0)

                if letter == "BLACK":
                        print("Current screen is:", self.root.current)
                        self.current_screen().canvas.ask_update()

            # Corrispondenza del messaggio con il modello di risposta agli score
            answer = re.match(score_msg, tmp)
            if answer:
                ID     = answer.group(1)
                LETTER = answer.group(2)
                TIME   = answer.group(3)

                # Salvo la risposta in base al tempo
                self.saved_ans[int(TIME)] = [ID, LETTER]
                print("Answer message:", LETTER, " from ", self.dictIDName[ID], " at time ", TIME)

                # Aggiornamento stato batteria
                if answer.group(5):
                    self.BATTERY_STATUS[ID] = int(answer.group(5))

            # Corrispondenza per i tempi
            time = re.match(timenow_msg, tmp)
            if time:
                time = time.group(1)
                print("--- Time ---------------------:", time)
                self.times.append(int(time))
                if self.startTimeGiven is True:
                    self.stop_time = int(time)
                else:
                    self.start_time = int(time)
                    self.startTimeGiven = True

            # Corrispondenza per la topologia
            topo = re.match(topology_msg, tmp)
            if topo:
                topo = topo.group(1)
                print("")
                print("MASTER")
                level = 0
                tmpStr = ""
                for i in range(len(topo)):
                    if topo[i] == '[':
                        level+=1
                    elif topo[i] == ']':
                        level-=1
                    elif topo[i].isdigit():
                        tmpStr += topo[i]
                    elif topo[i] == ',' and topo[i-1] != '}':
                        for i in range(level-1):
                            sys.stdout.write("   ")
                        try:
                            tmpStr = self.dictIDLastName[tmpStr]
                        except:
                            if tmpStr == "2131961277":
                                tmpStr = "CONTROLLER"
                        print("\\__" + tmpStr)
                        tmpStr = ""
                print("")
                self.topologyRead = True

    def on_start(self):
        ''' Chiamato all'inizio del gioco, carica la schermata
        '''
        self.load_screen('FirstScreen')

    def on_stop(self):
        ''' Chiude la comunicazione
        '''
        #t.stop()
        if self.no_serial is False:
            self.master.cleanup()

    #adapted from pydelhi_mobile:
    # https://github.com/pydelhi/pydelhi_mobile
    def load_screen(self, screen, manager=None):
        """
        Carica una schermata nell'oggetto ScreenManager (Qui ha fatto tutto chatgpt)

        Questo metodo carica dinamicamente una schermata specificata
        nel gestore dello schermo (ScreenManager) dell'applicazione.
        Se la schermata specificata non è stata ancora caricata,
        carica il modulo della schermata dinamicamente.

        Parameters
        ----------
        self: self
            L'istanza attuale dell'applicazione.
        screen: str
            Il nome della schermata da caricare.
        manager: ScreenManager, optional
            Il gestore dello schermo in cui caricare la schermata.
            Se non specificato, viene utilizzato il gestore principale (self.root).

        Returns
        -------
            screen_instance: Screen
                L'istanza della schermata caricata.
        """

        # load screen modules dynamically
        # for example load_screen('LoginScreen')
        # will look for uix/screens/loginscreen
        # load LoginScreen
        manager = manager or self.root  # Usa il gestore principale se manager non è specificato
        module_path = screen.lower()    # Converte il nome della schermata
                                        # in minuscolo per cercare il modulo corrispondente

        if not hasattr(self, module_path):  # Verifica se la schermata è già stata caricata
        # Carica dinamicamente il modulo della schermata
            from importlib import util
            
            toolbox_specs = util.find_spec(module_path)
            toolbox = util.module_from_spec(toolbox_specs)
            toolbox_specs.loader.exec_module(toolbox)
            screen_class = getattr(toolbox, screen)

            # Crea un'istanza della schermata e la aggiunge al gestore dello schermo
            sc = screen_class()

            # Salva l'istanza della schermata nell'attributo corrispondente dell'oggetto principale
            setattr(self, module_path, sc)
            manager.add_widget(sc)
        else:
            sc = getattr(self, module_path) # Se la schermata è già stata caricata,
                                            # recupera l'istanza dalla cache
        manager.current = screen            # Imposta la schermata appena caricata come
                                            # corrente nel gestore dello schermo
        return getattr(self, module_path)   # Restituisce l'istanza della schermata caricata


    def current_screen(self, manager=None):
        ''' Restituisce la schermata corrente
        '''
        manager = manager or self.root
        return manager.current_screen


    def do_backup(self):
        '''
        Salva un backup dei dati attuali su un file di backup.

        Questo metodo salva un backup dei dati attuali su un file di backup chiamato 'backup.dat'.
        I dati includono il numero totale e parziale delle domande,
        lo stato di avanzamento delle sezioni,
        lo storico delle risposte, lo stato delle assenze,
        il punteggio generale, il punteggio delle domande,
        il punteggio delle sezioni,
        le risposte date, i vincitori delle sezioni, i nomi delle prime sezioni,
        il nuovo punteggio e le domande ordinate.

        Parameters:
        -----------
        self: self
            L'istanza attuale dell'applicazione.

        Returns:
        --------
            None
        '''
        # Salvataggio del backup
        # Apertura del file di backup in modalità di scrittura
        savefile = open(self.filepath+'/backup.dat', 'w')
        tot_cnt_bak = self.QST_TOT_CNT+1  # Numero totale delle domande nel backup
        par_cnt_bak = self.QST_PAR_CNT+1  # Numero parziale delle domande nel backup
        sec_cnt_bak = self.SEC_CNT        # Numero di sezioni nel backup
        nor_cnt_bak = self.QST_NOR_CNT+1  # Numero normale delle domande nel backup
        dsp_cnt_bak = str(nor_cnt_bak)    # Numero visualizzato delle domande nel backup

        # Verifica se è necessario passare alla prossima sezione nel backup
        if par_cnt_bak == len(self.QUESTIONS[self.SEC_CNT].keys()):
            par_cnt_bak = 0
            sec_cnt_bak += 1

        # Conversione dei dati in formato JSON per il backup
        savestringa = json.dumps([dsp_cnt_bak, nor_cnt_bak, tot_cnt_bak, par_cnt_bak, sec_cnt_bak,
                                  self.HISTORY, self.ABSTENTIONS, self.GENERAL_SCORE,
                                  self.QUESTION_SCORE, self.SECTION_SCORE, self.ANSWERS_GIVEN,
                                  self.WINNER_OF_SECTIONS, self.SCT_FIRST_NAMES, self.score_new,
                                  self.sorted_x])

        savefile.write(savestringa) # Scrittura dei dati di backup nel file
        savefile.close()            # Chiusura del file di backup
        print("Backup written!!")   # Messaggio di conferma del backup avvenuto con successo


if __name__ == '__main__':
    BDCApp().run()
    
