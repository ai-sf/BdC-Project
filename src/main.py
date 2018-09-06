# -*- coding: utf8 -*-
'''
BOTTA DI COULOMB

AISF (Associazione Italiana Studenti di Fisica)
Comitato Locale di Pavia

Github Repo: http://github.com/
'''

__version__ = '1.0.0'

import serial
port_name = "/dev/ttyUSB0"

import os, sys, time
script_path = os.path.dirname(os.path.realpath(__file__))
os.environ['KIVY_WINDOW'] = 'sdl2'

music_path = script_path + '/music/'
img_path = script_path + '/img/'
icons_path = script_path + '/volti_fisici/'
# add module path for screen
module_path = script_path + '/uix/'
sys.path.insert(0, module_path)

# import App this is the main Class that manages UI's event loop
from kivy.app import App
from kivy.properties import NumericProperty, ListProperty, DictProperty, OptionProperty

#disable red point which appears with dx touch
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class Master:

    def __init__(self):
        try:
            self.ser = serial.Serial(port_name, 115200, timeout=None)
        except:
            print("Connection to serial port failed")
            exit()

    def write(self, string):
        self.ser.write(string)

    def cleanup(self):
        self.ser.close()

class BDCApp(App):

    #------------------
    TOTAL_TIME = 15
    #------------------

    dictANS={'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}

    end_score = False

    score_qst_ready = False
    score_gen_ready = False
    qst_done = False

    serial_message = ''

    icons_path = script_path + '/volti_fisici/'

    QST_DSP_CNT = NumericProperty(1)
    QST_TOT_CNT = NumericProperty(0)
    QST_PAR_CNT = NumericProperty(0)
    QUESTIONS = []

    SEC_CNT = NumericProperty(0)
    SECTIONS = []

    HISTORY = []

    ABSTENTIONS = {}
    # dictionary: { id :  score, ... }
    GENERAL_SCORE = {}
    # list of dictionary: [ { id : [score, time], ... } ...] with len(list) = number of questions
    QUESTION_SCORE = []
    # dictionary of dictionary: { section : { id : score, ... } ...} with len(list) = number of sections
    SECTION_SCORE = []
    # dictionary of list { id : [answer to qst 1, answer to qst 2, ...] }
    # 'None' means abstention
    ANSWERS_GIVEN = []

    saved_ans = {}
    times = []

    start_time = None
    stop_time = None
    startTimeGiven = False

    def build(self):

        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('config_file')
        args = parser.parse_args()

        from utils.user import setGlobal
        setGlobal(args.config_file)

        self.ABSTENTIONS = dict(zip(self.dictIDName.keys(),[0]*len(self.dictIDName.keys())))
        self.GENERAL_SCORE = dict(zip(self.dictIDName.keys(),[0]*len(self.dictIDName.keys())))
        print self.GENERAL_SCORE

        self.RisposteDateList = [[0,0,0,0,0]]*self.starting_counter
        self.RisposteOK = [0] * self.NUMERO_GIOCATORI

        #music
        from kivy.core.audio import SoundLoader
        self.dance = SoundLoader.load(music_path+'bensound-dance.wav')
        self.dance.volume = 0.5
        self.dance.loop = True
        self.dance.play()
        self.timer = SoundLoader.load(music_path+'audio_risposta_15s.wav')
        self.timer.loop = False
        self.scifi = SoundLoader.load(music_path+'bensound-scifi.wav')
        self.scifi.volume = 0.5
        self.scifi.loop = True

        if not self.NOCONTROLLER:
            self.master = Master()
            import threading
            t = threading.Thread(target=self.readserial)
            t.daemon = True
            t.start()

        from uix.screenmanager import BDCScreenManager
        sm = BDCScreenManager()
        return sm

    def checkForTimeNow(self):
        time.sleep(0.05)
        if self.start_time is None:
            self.master.write('timeNow\n')

    def readserial(self):

        import re
        showman_msg = r"--- MESSAGE RECEIVED ---------:from=2131961277,msgText=(\w+),msgTime=\d+"
        score_msg = r"--- MESSAGE RECEIVED ---------:from=(\d{10}),msgText=([ABCDE]),msgTime=(\d+)"
        timenow_msg = r"--- TIME NOW -----------------:timeNow=(\d+)"

        while True:
            tmp = self.master.ser.readline()

            letter = re.match(showman_msg, tmp)
            if letter:
                letter = letter.group(1)
                print "Showman:", letter
                if letter == "RED":
                    if hasattr(self.current_screen(), "next_button"):
                        if not self.current_screen().next_button.disabled:
                            self.current_screen().next_button.trigger_action()
                if letter == "GREEN":
                    if hasattr(self.current_screen(), "back_button"):
                        if not self.current_screen().back_button.disabled:
                            self.current_screen().back_button.trigger_action()
                if letter == "YELLOW":
                    if hasattr(self.current_screen(), "jolly_button"):
                        if not self.current_screen().jolly_button.disabled:
                            self.current_screen().jolly_button.trigger_action()
                if letter == "WHITE":
                        print("Current screen is:", self.root.current)
                        self.current_screen().canvas.ask_update()

            answer = re.match(score_msg, tmp)
            if answer:
                ID = answer.group(1)
                LETTER = answer.group(2)
                TIME = answer.group(3)
                self.saved_ans[int(TIME)] = [ID, LETTER]
                print "Answer message:", LETTER, " from ", self.dictIDName[ID], " at time ", TIME

            time = re.match(timenow_msg, tmp)
            if time:
                time = time.group(1)
                print "--- Time ---------------------:", time
                self.times.append(int(time))
                if self.startTimeGiven is True:
                    self.stop_time = int(time)
                else:
                    self.start_time = int(time)
                    self.startTimeGiven = True

    def on_start(self):
        self.load_screen('FirstScreen')

    def on_stop(self):
        t.stop()
        self.master.cleanup()

    #adapted from pydelhi_mobile
    def load_screen(self, screen, manager=None):
        manager = manager or self.root
        # load screen modules dynamically
        # for example load_screen('LoginScreen')
        # will look for uix/screens/loginscreen
        # load LoginScreen
        module_path = screen.lower()
        if not hasattr(self, module_path):
            import imp
            module = imp.load_module(screen, *imp.find_module(module_path))
            screen_class = getattr(module, screen)
            sc = screen_class()
            setattr(self, module_path, sc)
            manager.add_widget(sc)
        else:
            sc = getattr(self, module_path)
        manager.current = screen
        return getattr(self, module_path)

    def current_screen(self, manager=None):
        manager = manager or self.root
        return manager.current_screen

if __name__ == '__main__':
    BDCApp().run()
