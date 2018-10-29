from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

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
    back_button: dom_temp.clock.label
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
	circleColor: 0, 0.5, 0
	canvas:
		Color:
			rgb: self.circleColor
		Ellipse:
			pos: self.center_x-self.width*0.5, self.center_y-self.width*0.5
			size: self.width, self.width
			angle_start: 0
			angle_end: self.angle_end
""")


class CircleTime(Widget):

    circle = ObjectProperty(None)
    count = 1

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
		center_y: root.center_y
		color: 1,1,1,1
		font_size: 80*app.scalatore
		background_normal: ''
		background_down: ''
		background_color: 0,0,0,0
		on_press: root.parent.start_time()
    """)

    def update(self, dt):
        if self.count <= app.clock_steps:
            self.label.text = ''
            self.circle.angle_end = 360 - self.count*(360.0/app.clock_steps)
            #self.label.text = str(10 - self.count)
            if self.count > float(app.clock_steps)/2:
                self.circle.circleColor = (1,1,0)
            if self.count > float(app.clock_steps)*3/4:
                self.circle.circleColor = (1,0,0)
            self.count += 1
        else:
            self.parent.time_finished = True
            self.label.text = '0'
            self.label.color = [1,0,0,1]
            #self.parent.show_right_answer_button.disabled = False
            return False

    def reset(self):
        self.circle.angle_end = 360
        self.circle.circleColor = (0,0.5,0)
        self.label.text = str(app.QST_DSP_CNT)
        self.label.color = [1,1,1,1]
        self.label.disabled = False
        self.count = 1

class Domanda(GridLayout):

    MODE = StringProperty('OFF_BF')
    ans_opacity = { 'OFF_BF' : 0, 'ON' : 1, 'OFF_AF' : 1}
    side_opacity = { 'OFF_BF' : 0, 'ON' : 0, 'OFF_AF' : 1}
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

    #start_time_button = ObjectProperty(None)

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
		font_name: 'UbuntuMono-B.ttf'
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
        text: 'A'
        disabled: True
        disabled_color: 0,0.8,0,1
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
        text: 'B'
        disabled: True
        disabled_color: 1,1,1,1
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
        text: 'C'
        disabled: True
        disabled_color: 0.8,0,0,1
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
        text: 'D'
        disabled: True
        disabled_color: 1,0.75,0.095,1
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
        text: 'E'
        disabled: True
        disabled_color: 0,0.4,1,1
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
		on_press: root.show_terna(); root.show_answer()
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

        print("Domanda visualizzata: "+str(app.QST_DSP_CNT))
        print("Sezione: "+str(app.SEC_CNT+1)+"/"+str(len(app.SECTIONS)))
        print("Domanda in sezione: "+str(app.QST_PAR_CNT+1)+"/"+str(len(app.QUESTIONS[app.SEC_CNT].keys())))

        self.MODE = 'ON'

        self.clock.label.disabled = True

        #rest variables for input
        app.saved_ans = {}
        app.times = []
        app.startTimeGiven = False

        #we want to be sure the message is received
        if app.NOCONTROLLER is False:
            app.master.write('timeNow\n')
        app.checkForTimeNow()

        Clock.schedule_once(self.writetimenow, app.TOTAL_TIME)

        app.scifi.stop()

        if app.TOTAL_TIME == 15:
            app.timer.play()
            Clock.schedule_once(self.stop_audio, app.timer.length)

        Clock.schedule_once(self.end_time, app.TOTAL_TIME+5)
        Clock.schedule_interval(self.clock.update, float(app.TOTAL_TIME)/app.clock_steps)
        Clock.schedule_once(self.sendRAW, app.TOTAL_TIME+6)

    def writetimenow(self,dt):
        if app.NOCONTROLLER is False:
            app.master.write('timeNow\n')

    def stop_audio(self,dt):
        app.timer.stop()

    def sendRAW(self, dt):
        for key, value in self.RAWdic.iteritems():
            if app.NOCONTROLLER is False:
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

        if app.NOCONTROLLER is True:
            risposte_date = DictOfAnswers_fake()
        else:
            risposte_date = DictOfAnswers()

        result = result(risposte_date)

        self.RAWdic = update_score(result, 'RAWdic')
        RAW = update_score(result, 'ans')
        app.HISTORY.append(risposte_date)

        #creating button's text
        self.terna_risultato = '[color=008000]:-) '+str(RAW['R'])+'[/color][color=FF0000]   :-( '+str(RAW['W'])+'[/color][color=FFE118]   :-| '+str(RAW['A'])+'[/color]'

        # #saving statistics
        # with open(filenameTime,'r') as f:
        #     statcontent = f.read()
        # if statcontent == '':
        #     statlist = []
        # else:
        #     statlist = json.loads(statcontent)
        # statlist.append(risposte_date)
        # statfile = open(filenameTime,'w')
        # statstringa = json.dumps(statlist)
        # print statstringa
        # statfile.truncate(0)
        # statfile.write(statstringa)
        # statfile.close()

        ##################################################

        time.sleep(0.5)

        self.show_terna()
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
        stringRIGHT_button = 'side'+str(rightans)+'_button'
        exec("self."+stringRIGHT_button+".background_color=[0,0.4,0,1]")

    def show_terna(self):
        self.showterna_button.text = self.terna_risultato
        rightans = app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['OK']
        risp_button = 'ans'+str(rightans)+'_button'
        exec("self."+risp_button+".background_color=[0,0.4,0,1]")
        letter_button = 'label'+str(rightans)+'_button'
        exec("self."+letter_button+".background_color=[0,0.4,0,1]")

    # def printprova(self, name):
    #     if self.debuganswergiven == False:
    #         timediff = time.time() - self.debugstarttime
    #         giustastr = 'ESATTA' if name==RispostaOKList[self.question_counter-1] else 'SBAGLIATA'
    #         print 'Domanda #'+str(self.question_counter)+': label '+name+', time '+ str(timediff)+' - '+giustastr
    #         exec("self.risposta"+name+"_button.text+=' (DATA!)'")
    #         self.debuganswergiven = True


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
