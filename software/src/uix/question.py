from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from math import *

import operator
import time
import json

app = App.get_running_app()

import sys
sys.path.insert(0, app.main_path)
import iconfonts.iconfonts as iconfonts

class Question(Screen):

    Builder.load_string("""
<Question>:

    name: 'Question'

    next_button: dom_temp.spiegazione_button
    jolly_button: dom_temp.classdom_button
    timer_button: dom_temp.clock.label
	id_dom: dom_temp

	Domanda:
		id: dom_temp
""")

    def on_enter(self):
        if app.qst_done:
            pass
        else:
            self.id_dom.update_question()
            app.dance.stop()
            app.scifi.play()

class Circle(Widget):
    Builder.load_string("""
<Circle>:
	angle_end: 360
	circleColorBig: 1, 1, 1
	canvas:
		Color:
			rgb: self.circleColorBig
		Ellipse:
			pos: self.center_x-self.width*9/10*0.5, self.center_y-self.width*9/10*0.5
			size: self.width*9/10, self.width*9/10
			angle_start: 0
			angle_end: self.angle_end

<Circle>:
	angle_end: 360
	circleColor: 0.2, 0.2, 0.2
	canvas:
		Color:
			rgb: self.circleColor
		Ellipse:
			pos: self.center_x-self.width*7/9*0.5, self.center_y-self.width*7/9*0.5
			size: self.width*7/9, self.width*7/9
			angle_start: 0
			angle_end: self.angle_end
""")


class CircleTime(Widget):

    circle = ObjectProperty(None)
    count = 1

    sound_status = ObjectProperty(None)

    Builder.load_string("""
<CircleTime>:
	circle: circle_temp
	label: button_temp
	Circle:
		id: circle_temp
		pos: root.pos
		size: root.size
	Button:
		id: button_temp
		center_x: root.center_x
		center_y: root.center_y+root.width/22
		color: 1,1,1,1
        outline_color: 0,0,0,1
        outline_width: 10
		font_size: 80*app.scalatore

		background_normal: ''
		background_down: ''
		background_color: 0,0,0,0
		on_press: root.parent.start_time()
    """)

    def update(self, dt):
        if self.count <= app.clock_steps:
            if app.show_timer:
                if app.QUESTION_TOTAL_TIME < 60:
                    self.label.text = str(int((300-self.count)*app.QUESTION_TOTAL_TIME/300.)+1)
                    self.end_time_text = '0'
                else:
                    if int(((300-self.count)*app.QUESTION_TOTAL_TIME/300.)+1)%60 < 10:
                        zeroIfNeeded = '0'
                    else:
                        zeroIfNeeded = ''
                    self.label.text = str(int(((300-self.count)*app.QUESTION_TOTAL_TIME/300.)+1)/60)+":"+zeroIfNeeded+str(int(((300-self.count)*app.QUESTION_TOTAL_TIME/300.)+1)%60)
                    self.label.font_size = 50*app.scalatore
                    self.end_time_text = '0:00'
            else:
                self.label.text = ''
            self.circle.angle_end = 360 - self.count*(360.0/app.clock_steps)

            #suono e colore timer
            if app.QUESTION_TOTAL_TIME <= 60:

                if self.count <= float(app.clock_steps)/3:

                    if self.sound_status == 0:
                        app.timer_slow.play()
                        app.timer_slow.loop = True
                        self.sound_status = 1
                    app.timer_slow.volume = self.count*3/float(app.clock_steps)

                    self.circle.circleColor = (0,0.2,0)
                    self.circle.circleColorBig = (0,1,0)
                    self.label.color = [0,1,0,1]

                elif self.count <= float(app.clock_steps)*2/3:

                    self.circle.circleColor = (0.15,0.15,0)
                    self.circle.circleColorBig = (1,1,0)
                    self.label.color = [1,1,0,1]

                else:

                    if self.sound_status == 1:
                        app.timer_slow.stop()
                        app.timer_slow.loop = False
                        app.timer_fast.play()
                        app.timer_fast.loop = True
                        self.sound_status = 2

                    self.circle.circleColor = (0.2,0,0)
                    self.circle.circleColorBig = (1,0,0)
                    self.label.color = [1,0,0,1]

            else:

                if self.count <= (1-(60/float(app.QUESTION_TOTAL_TIME)))*app.clock_steps:

                    self.circle.circleColor = (0,0.2,0)
                    self.circle.circleColorBig = (0,1,0)
                    self.label.color = [0,1,0,1]

                else:

                    if self.count <= (1-(40/float(app.QUESTION_TOTAL_TIME)))*app.clock_steps:

                        if self.sound_status == 0:
                            app.timer_slow.play()
                            app.timer_slow.loop = True
                            self.sound_status = 1
                        app.timer_slow.volume = (self.count-((1-(60/float(app.QUESTION_TOTAL_TIME)))*app.clock_steps))/((20/float(app.QUESTION_TOTAL_TIME))*app.clock_steps)

                        self.circle.circleColor = (0,0.2,0)
                        self.circle.circleColorBig = (0,1,0)
                        self.label.color = [0,1,0,1]

                    elif self.count <= (1-(20/float(app.QUESTION_TOTAL_TIME)))*app.clock_steps:

                        self.circle.circleColor = (0.15,0.15,0)
                        self.circle.circleColorBig = (1,1,0)
                        self.label.color = [1,1,0,1]

                    else:

                        if self.sound_status == 1:
                            app.timer_slow.stop()
                            app.timer_slow.loop = False
                            app.timer_fast.play()
                            app.timer_fast.loop = True
                            self.sound_status = 2

                        self.circle.circleColor = (0.2,0,0)
                        self.circle.circleColorBig = (1,0,0)
                        self.label.color = [1,0,0,1]

            self.count += 1

        else:
            app.timer_slow.stop()
            app.timer_slow.loop = False
            app.timer_fast.stop()
            app.timer_fast.loop = False
            app.timer_gong.play()
            self.parent.time_finished = True
            self.label.text = self.end_time_text
            self.label.color = [1,0,0,1]
            return False

    def reset(self):
        self.circle.angle_end = 360
        self.circle.circleColor = (0.2,0.2,0.2)
        self.circle.circleColorBig = (1,1,1)
        self.label.text = str(app.QST_DSP_CNT)
        self.label.color = [1,1,1,1]
        self.label.disabled = False
        self.count = 1
        self.sound_status = 0
        self.label.font_size = 80*app.scalatore

class Domanda(GridLayout):

    MODE = StringProperty('OFF_BF')
    ans_opacity = { 'OFF_BF' : 0, 'ON' : 1, 'OFF_AF' : 1}
    side_opacity = { 'OFF_BF' : 0, 'ON' : 0, 'OFF_AF' : 1}
    label_opacity = { 'OFF_BF' : 1, 'ON' : 1, 'OFF_AF' : 1}
    label_text_opacity = { 'OFF_BF' : 1, 'ON' : 1, 'OFF_AF' : 1}
    bkg_color_label = { 'OFF_BF' : [162,162,162,0.1], 'ON' : [162,162,162,0.1], 'OFF_AF' : [1,1,1,1] }
    bkg_color_answer = { 'OFF_BF' : [0,0,0,1], 'ON' : [0,0,0,1], 'OFF_AF' : [1,1,1,1] }
    bkg_color_side = { 'OFF_BF' : [162,162,162,0], 'ON' : [162,162,162,0], 'OFF_AF' : [1,1,1,1] }

    time_finished = True

    clock = ObjectProperty(None)

    labelA_button = ObjectProperty(None)
    labelB_button = ObjectProperty(None)
    labelC_button = ObjectProperty(None)
    labelD_button = ObjectProperty(None)
    labelE_button = ObjectProperty(None)

    domanda_button = ObjectProperty(None)
    rispostaA_button = ObjectProperty(None)
    rispostaB_button = ObjectProperty(None)
    rispostaC_button = ObjectProperty(None)
    rispostaD_button = ObjectProperty(None)
    rispostaE_button = ObjectProperty(None)

    sideA_button = ObjectProperty(None)
    sideB_button = ObjectProperty(None)
    sideC_button = ObjectProperty(None)
    sideD_button = ObjectProperty(None)
    sideE_button = ObjectProperty(None)

    showterna_button = ObjectProperty(None)

    spiegazione_button = ObjectProperty(None)
    dettrisp_button = ObjectProperty(None)
    classdom_button = ObjectProperty(None)
    classgen_button = ObjectProperty(None)

    terna_risultato = ':-) 0 :-( 0 :-| 0'

    debugstarttime = 0
    debuganswergiven = False

    firstthread = True

    finedomandeprova = BooleanProperty(False)

    app.A_color = [0.0,0.8,0.0,1]
    app.B_color = [1.0,1.0,1.0,1]
    app.C_color = [0.8,0.0,0.0,1]
    app.D_color = [1.0,0.8,0.1,1]
    app.E_color = [0.0,0.4,1.0,1]

    Builder.load_string("""
<Domanda>:

	clock: clock_temp
	domanda_button: domanda_button_temp
    start_time_button: start_time_button_temp

	labelA_button: labelA_temp
	labelB_button: labelB_temp
	labelC_button: labelC_temp
	labelD_button: labelD_temp
	labelE_button: labelE_temp

	ansA_button: ansA_temp
	ansB_button: ansB_temp
	ansC_button: ansC_temp
	ansD_button: ansD_temp
	ansE_button: ansE_temp

	sideA_button: sideA_temp
	sideB_button: sideB_temp
	sideC_button: sideC_temp
	sideD_button: sideD_temp
	sideE_button: sideE_temp

	spiegazione_button: spiegazione_button_temp
	showterna_button: showterna_button_temp
	classdom_button: classdom_button_temp

	cols: 3
    rows: 7

	rows_minimum: {0: 2*self.height/8, 1: self.height/8, 2: self.height/8,  3: self.height/8, 4: self.height/8,  5: self.height/8, 6: self.height/8}

	CircleTime:
		id: clock_temp
		size_hint_x: None
		width: root.width / 8
	Button:
		id: domanda_button_temp
		text: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['qst']
		bold: True
#		font_name: 'Ubuntu-L.ttf'
		font_size: 35 * app.scalatore
		halign: 'center'
		valign: 'middle'
#		size_hint_y: None
		text_size: self.width, None
#		height: self.texture_size[1]
		background_down: app.SECTIONS[app.SEC_CNT]['bkg']
		background_normal: app.SECTIONS[app.SEC_CNT]['bkg']

        background_color: 1,1,1,0.5
		height: 7* root.height / 9
		padding_x: 0.05*self.width
		markup: True
	Button:
		#395x500
		id: spiegazione_button_temp
		disabled: True
		text: '?'
		disabled_color: 1,1,1,1
		font_size: 150*app.scalatore
		font_name: 'font/UbuntuMono-B.ttf'
        #padding_x: 0.5*self.width
		background_disabled_down: ''
		background_disabled_normal: ''
		background_down: 'img/bulb.png'
		background_normal: 'img/bulb.png'
		background_color: 0,0,0,0
		size_hint_x: None
		width: root.parent.width / 9
		on_press: app.load_screen('AfterQstSlides')
# A #--------------------------------------------------------------------------
	LabelButton:
		id: labelA_temp
        font_name: 'font/Symbola.ttf'
        font_size: 120 * app.scalatore
        text: u'\u24b6'
        disabled: True
        disabled_color: app.A_color[0],app.A_color[1],app.A_color[2],root.label_text_opacity[root.MODE]
        opacity: root.label_opacity[root.MODE]
        background_color: root.bkg_color_label[root.MODE]
	AnswerButton:
        id: ansA_temp
        text: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['ans'][0]
        disabled: True
        background_color: root.bkg_color_answer[root.MODE]
        opacity: root.ans_opacity[root.MODE]
#       on_press: root.printprova('A')
	SideButton:
		id: sideA_temp
        text: 'A'
        disabled: True
        background_color: root.bkg_color_side[root.MODE]
        opacity: root.side_opacity[root.MODE]
# B #--------------------------------------------------------------------------
	LabelButton:
		id: labelB_temp
        font_name: 'font/Symbola.ttf'
        font_size: 120 * app.scalatore
        text: u'\u24b7'
        disabled: True
        disabled_color: app.B_color[0],app.B_color[1],app.B_color[2],root.label_text_opacity[root.MODE]
        opacity: root.label_opacity[root.MODE]
        background_color: root.bkg_color_label[root.MODE]
	AnswerButton:
        id: ansB_temp
        text: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['ans'][1]
        disabled: True
        background_color: root.bkg_color_answer[root.MODE]
        opacity: root.ans_opacity[root.MODE]
#       on_press: root.printprova('B')
	SideButton:
		id: sideB_temp
        text: 'B'
        disabled: True
        background_color: root.bkg_color_side[root.MODE]
        opacity: root.side_opacity[root.MODE]
# C #--------------------------------------------------------------------------
	LabelButton:
		id: labelC_temp
        font_name: 'font/Symbola.ttf'
        font_size: 120 * app.scalatore
        text: u'\u24b8'
        disabled: True
        disabled_color: app.C_color[0],app.C_color[1],app.C_color[2],root.label_text_opacity[root.MODE]
        opacity: root.label_opacity[root.MODE]
        background_color: root.bkg_color_label[root.MODE]
	AnswerButton:
        id: ansC_temp
        text: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['ans'][2]
        disabled: True
        opacity: root.ans_opacity[root.MODE]
        background_color: root.bkg_color_answer[root.MODE]
#       on_press: root.printprova('C')
	SideButton:
		id: sideC_temp
        text: 'C'
        disabled: True
        opacity: root.side_opacity[root.MODE]
        background_color: root.bkg_color_side[root.MODE]
# D #--------------------------------------------------------------------------
	LabelButton:
		id: labelD_temp
        font_name: 'font/Symbola.ttf'
        font_size: 120 * app.scalatore
        text: u'\u24b9'
        disabled: True
        disabled_color: app.D_color[0],app.D_color[1],app.D_color[2],root.label_text_opacity[root.MODE]
        opacity: root.label_opacity[root.MODE]
        background_color: root.bkg_color_label[root.MODE]
	AnswerButton:
        id: ansD_temp
        text: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['ans'][3]
        disabled: True
        opacity: root.ans_opacity[root.MODE]
        background_color: root.bkg_color_answer[root.MODE]
#       on_press: root.printprova('D')
	SideButton:
		id: sideD_temp
        text: 'D'
        disabled: True
        opacity: root.side_opacity[root.MODE]
        background_color: root.bkg_color_side[root.MODE]
# E #--------------------------------------------------------------------------
	LabelButton:
		id: labelE_temp
        font_name: 'font/Symbola.ttf'
        font_size: 120 * app.scalatore
        text: u'\u24ba'
        disabled: True
        disabled_color: app.E_color[0],app.E_color[1],app.E_color[2],root.label_text_opacity[root.MODE]
        opacity: root.label_opacity[root.MODE]
        background_color: root.bkg_color_label[root.MODE]
	AnswerButton:
        id: ansE_temp
        text: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['ans'][4]
        disabled: True
        opacity: root.ans_opacity[root.MODE]
        background_color: root.bkg_color_answer[root.MODE]
#       on_press: root.printprova('E')
	SideButton:
		id: sideE_temp
        text: 'E'
        disabled: True
        opacity: root.side_opacity[root.MODE]
        background_color: root.bkg_color_side[root.MODE]
#------------------------------------------------------------------------------
	SideButton:
		id: start_time_button_temp
		disabled: True
		background_disabled_down: 'img/logoBdC_bianco.png'
		background_disabled_normal: 'img/logoBdC_bianco.png'
		background_color: 1,1,1,1
		size_hint_x: None
		width: root.width / 8
    Button:
		id: showterna_button_temp
		text: 'VEDI RISPOSTE!'
		bold: True
		markup: True
		disabled: True
		on_press: root.show_answer()
		background_normal: ''
		background_color: 162,162,162,0
		font_size: 50*app.scalatore
	SideButton:
		#450x285
		id: classdom_button_temp
		disabled: True
		background_disabled_down: ''
		background_disabled_normal: ''
		background_down: 'img/scoreboard.png'
		background_normal: 'img/scoreboard.png'
		background_color: 0,0,0,0
		size_hint_x: None
		width: root.parent.width / 9
		on_press: app.load_screen('ScoreQstScreen')
        """)

    def update_question(self):

        try:
            app.QUESTION_TOTAL_TIME = int(app.SECTIONS[app.SEC_CNT]['time'])
        except:
            app.QUESTION_TOTAL_TIME = app.TOTAL_TIME

        self.MODE = 'OFF_BF'

        self.clock.reset()

        self.showterna_button.disabled = True
        self.spiegazione_button.disabled = True
        self.classdom_button.disabled = True
        self.showterna_button.text = ''
        self.spiegazione_button.background_color = [0,0,0,0]
        self.classdom_button.background_color = [0,0,0,0]

        # if special section, then icon instead of '?'
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            ic = app.SECTIONS[app.SEC_CNT]['icon']
            self.spiegazione_button.markup = True
            self.spiegazione_button.text = "%s"%(iconfonts.icon(ic))
        else:
            self.spiegazione_button.markup = False
            self.spiegazione_button.text = '?'

    def start_time(self):

        print("\033[1;97m\033[1;100m")
        print("STATO DOMANDE ----------------------------------\n")
        if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            domanda_str = str(app.QST_DSP_CNT) + str(app.QST_PAR_CNT+1)
        else:
            domanda_str = str(app.QST_DSP_CNT)
        domanda_str += "/"
        tot_domande = app.NUM_OF_QST
        if app.SECTIONS[0]['type'] == 'test':
            tot_domande -= len(app.QUESTIONS[0])
        domanda_str += str(tot_domande)
        print("Domanda visualizzata: \033[1;92m"+domanda_str)
        print("\033[1;97m        Tipo sezione: \033[1;92m"+str(app.SECTIONS[app.SEC_CNT]['type']))
        print("\033[1;97m  Domanda in sezione: \033[1;92m"+str(app.QST_PAR_CNT+1)+"/"+str(len(app.QUESTIONS[app.SEC_CNT].keys())))
        print("\033[1;97m      Numero sezione: \033[1;92m"+str(app.SEC_CNT+1)+"/"+str(len(app.SECTIONS)))
        print("\033[0m\n")

        self.MODE = 'ON'

        self.clock.label.disabled = True

        #rest variables for input
        app.saved_ans = {}
        app.times = []
        app.startTimeGiven = False

        #we want to be sure the message is received
        if app.no_serial is False:
            app.master.write('timeNow\n')
        app.checkForTimeNow()

        if app.QUESTION_TOTAL_TIME > 0:
            Clock.schedule_once(self.writetimenow, app.QUESTION_TOTAL_TIME)
            Clock.schedule_once(self.end_time, app.QUESTION_TOTAL_TIME+5)
            Clock.schedule_interval(self.clock.update, float(app.QUESTION_TOTAL_TIME)/app.clock_steps)
            Clock.schedule_once(self.sendRAW, app.QUESTION_TOTAL_TIME+6)
        else:
            self.end_time(self)
            self.clock.update(self)

        app.scifi.stop()

    def writetimenow(self,dt):
        if app.no_serial is False:
            app.master.write('timeNow\n')

    def sendRAW(self, dt):
        for key, value in self.RAWdic.items():
            if app.no_serial is False:
                app.master.write('send '+key+' '+value+'\n')
            time.sleep(0.05)

    def end_time(self, dt):

        app.dance.play()

        self.spiegazione_button.disabled = False
        self.spiegazione_button.background_color = [1,1,1,1]
        self.spiegazione_button.text = ''
        self.classdom_button.disabled = False
        self.classdom_button.background_color = [1,1,1,1]

        from utils.calculate_score import update_score, DictOfAnswers, DictOfAnswers_fake, result

        if app.no_serial is True:
            risposte_date = DictOfAnswers_fake()
        else:
            risposte_date = DictOfAnswers()

        result = result(risposte_date)

        self.RAWdic = update_score(result, 'RAWdic')
        RAW = update_score(result, 'ans')
        app.HISTORY.append(risposte_date)
        app.lastRisposteDate = risposte_date

        #creating button's text
        self.terna_risultato = '[color=00cc00]%s'%(iconfonts.icon('fa-check-circle'))+' '+str(RAW['R'])+'      '+'[/color][color=ff0000]%s'%(iconfonts.icon('fa-times-circle'))+' '+str(RAW['W'])+'      '+'[/color][color=ffcc00]%s'%(iconfonts.icon('fa-minus-circle'))+' '+str(RAW['A'])+'[/color]'

        app.qst_done = True
        self.show_answer()

        app.score_qst_ready = False
        app.score_gen_ready = False

        app.Score = [(key, app.GENERAL_SCORE[key]) for key in app.GENERAL_SCORE.keys()]
        app.sorted_x = sorted(app.Score, key=operator.itemgetter(1), reverse= True)

        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            app.Score_sct = [(key, app.SECTION_SCORE[app.SEC_CNT][key]) for key in app.SECTION_SCORE[app.SEC_CNT].keys()]
            app.sorted_x_sct = sorted(app.Score_sct, key=operator.itemgetter(1), reverse= True)

        app.Position = {}
        for name in app.dictIDName.keys():
            app.Position[name] = [j[0] for j in app.sorted_x].index(name)

    def show_answer(self):

        rightans = app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['OK']

        count_ans = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

        for value in app.HISTORY[-1].values():
            label = value[0]
            if label in count_ans.keys():
                count_ans[label] += 1

        self.sideA_button.opacity = 1
        self.sideB_button.opacity = 1
        self.sideC_button.opacity = 1
        self.sideD_button.opacity = 1
        self.sideE_button.opacity = 1

        self.sideA_button.text = str(count_ans['A'])
        self.sideB_button.text = str(count_ans['B'])
        self.sideC_button.text = str(count_ans['C'])
        self.sideD_button.text = str(count_ans['D'])
        self.sideE_button.text = str(count_ans['E'])

        self.showterna_button.text = self.terna_risultato

        for l in ['A','B','C','D','E']:
            if l == str(rightans):
                exec("self.side"+l+"_button.background_color=[0,1,0.7,0.4]")
                exec("self.ans"+l+"_button.background_color=[0,1,0.7,0.4]")
                exec("self.label"+l+"_button.background_color=[0,1,0.7,0.4]")
            else:
                exec("self.side"+l+"_button.opacity=0.5")
                exec("self.ans"+l+"_button.opacity=0.5")
                exec("self.label"+l+"_button.opacity = 0.5")

class AnswerButton(Button):

    Builder.load_string("""
<AnswerButton>:
	text_size: self.size
	halign: 'left'
	valign: 'middle'
	max_lines: 2
	background_disabled_normal: ''
	background_disabled_down: ''
	font_size: 35*app.scalatore
	padding_x: 0.03*self.width
    disabled_color: 1,1,1,1
	markup: True
    """)

class SideButton(Button):

    Builder.load_string("""
<SideButton>:
	size_hint_x: None
	width: root.parent.width / 9
    background_normal: ''
	background_disabled_normal: ''
	background_disabled_down: ''
	halign: 'center'
	valign: 'middle'
	text_size: self.width, None
    font_size: 50*app.scalatore
	disabled_color: 1,1,1,1
    """)

class LabelButton(Button):

    Builder.load_string("""
<LabelButton>:
	size_hint_x: None
	width: root.parent.width / 8
	bold: True
	valign: 'middle'
	background_disabled_normal: ''
	background_disabled_down: ''
	font_size: 80*app.scalatore
	padding_x: 0.1*self.width
    """)
