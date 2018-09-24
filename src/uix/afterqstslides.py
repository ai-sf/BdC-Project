from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty

import json

app = App.get_running_app()

class AfterQstSlides(Screen):

    label_score = StringProperty('')
    slide_img = ObjectProperty(None)
    counter = NumericProperty(0)

    showScoreGen = BooleanProperty(True)

    next_button = ObjectProperty()
    jolly_button = ObjectProperty()
    back_button = ObjectProperty()

    Builder.load_string("""
<AfterQstSlides>:

    name: 'AfterQstSlides'

	slide_img: img_temp

    next_button: next_tmp
    jolly_button: score_tmp
    back_button: back_tmp

	StackLayout:
		orientation: 'lr-bt'

		Button:
            id: back_tmp
			size_hint: 1.0/3, 1.0/12
			text: "INDIETRO"
			text_size: self.size
			valign: 'middle'
			halign: 'center'
			font_size: 30*app.scalatore
			on_press: app.load_screen('Question')

		Button:
            id: score_tmp
			size_hint: 1.0/3, 1.0/12
			text: root.label_score
			text_size: self.size
			valign: 'middle'
			halign: 'center'
			font_size: 30*app.scalatore
			on_press: root.show_score()

		Button:
            id: next_tmp
			size_hint: 1.0/3, 1.0/12
			text: "-->"
			text_size: self.size
			valign: 'middle'
			halign: 'center'
			font_size: 30*app.scalatore
			on_press: root.next()

		Button:
			id: img_temp
			size_hint: 1, 11.0/12
			disabled: True
			background_disabled_down: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_af'][root.counter]
			background_disabled_normal: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_af'][root.counter]
    """)

    def on_enter(self):
        self.counter = 0
        if (app.NUM_OF_QST - app.QST_TOT_CNT) < 5:
            self.jolly_button.disabled = True
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            self.label_score = 'CLASSIFICA SEZIONE'
            if app.QST_PAR_CNT+1 == len(app.QUESTIONS[app.SEC_CNT].keys()):
                self.jolly_button.disabled = False
            else:
                self.jolly_button.disabled = True
        if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
            self.label_score = 'CLASSIFICA GENERALE'
        if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            self.label_score = 'CLASSIFICA GENERALE'

    def show_score(self):
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            app.load_screen('ScoreSctScreen')
        if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
            app.load_screen('ScoreGenScreen')
        if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            app.load_screen('ScoreGenScreen')

    def next(self):
        print("QST_DSP_CNT = "+str(app.QST_DSP_CNT))
        print("QST_NOR_CNT = "+str(app.QST_NOR_CNT))
        if self.counter+1 == len(app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_af']):
            app.QST_TOT_CNT += 1
            if app.QST_PAR_CNT+1 == len(app.QUESTIONS[app.SEC_CNT].keys()):
                app.QST_PAR_CNT = 0
                #-----------------------------------------------------------
                if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
                    # creating a list with the ids of the section winners
                    app.SCT_FIRST_NAMES = []
                    for idx in range(len(app.sorted_x_sct)):
                        app.SCT_FIRST_NAMES.append(app.sorted_x_sct[idx][0])
                        if idx+1 < len(app.sorted_x_sct):
                            if app.sorted_x_sct[idx][1] > app.sorted_x_sct[idx+1][1]:
                                break
                            else:
                                continue
                        else:
                            break
                    # assigning the icons and the money PRIZE
                    num_winner = len(app.SCT_FIRST_NAMES)
                    for winner in app.SCT_FIRST_NAMES:
                        if not app.WINNER_OF_SECTIONS.has_key(winner):
                            app.WINNER_OF_SECTIONS[winner] = [app.SECTIONS[app.SEC_CNT]['icon']]
                        else:
                            app.WINNER_OF_SECTIONS[winner].append(app.SECTIONS[app.SEC_CNT]['icon'])
                        app.GENERAL_SCORE[winner] += app.PRIZE/num_winner
                #-----------------------------------------------------------
                if app.SEC_CNT+1 == len(app.SECTIONS):
                    self.do_backup()
                    app.load_screen('LastScreen')
                else:
                    self.do_backup()
                    app.load_screen("ScoreGenFinScreen")
            else:
                if app.SECTIONS[app.SEC_CNT]['type'] == 'normal' or app.SECTIONS[app.SEC_CNT]['type'] == 'special':
                    app.QST_DSP_CNT = str(int(app.QST_DSP_CNT)+1)
                    app.QST_NOR_CNT += 1
                app.QST_PAR_CNT += 1
                self.do_backup()
                app.load_screen("BeforeQstSlides")
        else:
            self.counter +=1

    def do_backup(self):
        # #saving backup
        savefile = open(app.filepath+'/backup.dat','w')
        savestringa = json.dumps([app.QST_DSP_CNT, app.QST_NOR_CNT, app.QST_TOT_CNT, app.QST_PAR_CNT, app.SEC_CNT, app.HISTORY, app.ABSTENTIONS,app.GENERAL_SCORE, app.QUESTION_SCORE,app.SECTION_SCORE,app.ANSWERS_GIVEN])
        savefile.write(savestringa)
        savefile.close()
        print("Backup written!!")
