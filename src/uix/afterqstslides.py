from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
import operator
import json
import iconfonts.iconfonts as iconfonts

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

        self.next_button.markup = True
        self.next_button.text = "%s"%(iconfonts.icon('fa-forward'))
        self.next_button.font_size = 50*app.scalatore

        self.back_button.markup = True
        self.back_button.text = "%s"%(iconfonts.icon('fa-backward'))
        self.back_button.font_size = 50*app.scalatore

        self.jolly_button.markup = True
        self.jolly_button.font_size = 50*app.scalatore

        if (app.NUM_OF_QST - app.QST_TOT_CNT) <= 5 and app.SECTIONS[app.SEC_CNT]['type'] != 'test':
            self.jolly_button.disabled = True
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            ic = app.SECTIONS[app.SEC_CNT]['icon']
            self.label_score = "%s"%(iconfonts.icon('fa-list-ol')) + " " + "%s"%(iconfonts.icon(ic))
            if app.QST_PAR_CNT+1 == len(app.QUESTIONS[app.SEC_CNT].keys()):
                self.jolly_button.disabled = False
            else:
                self.jolly_button.disabled = True
        if app.SECTIONS[app.SEC_CNT]['type'] == 'normal' or app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            self.label_score = "%s"%(iconfonts.icon('fa-list-ol'))

    def show_score(self):
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            app.load_screen('ScoreSctScreen')
        if app.SECTIONS[app.SEC_CNT]['type'] == 'normal' or app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            app.load_screen('ScoreGenScreen')

    def next(self):
        if self.counter+1 == len(app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_af']):
            self.counter = 0
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

                    #print classifica generale dopo sezione speciale a terminale
                    Score_term = [(key, app.GENERAL_SCORE[key]) for key in app.GENERAL_SCORE.keys()]
                    sorted_x_term = sorted(Score_term, key=operator.itemgetter(1), reverse= True)
                    print "\033[1;97m\033[1;100m"
                    print "CLASSIFICA GENERALE ----------------------------"
                    print "                                AST     BAT"
                    for i in range(len(sorted_x_term)):
                        spacer = "\033[1;96m"
                        if sorted_x_term[i][1] >= 0:
                            if sorted_x_term[i][1] < 10000:
                                spacer += " "
                            if sorted_x_term[i][1] < 1000:
                                spacer += " "
                            if sorted_x_term[i][1] < 100:
                                spacer += " "
                            if sorted_x_term[i][1] < 10:
                                spacer += " "
                        else:
                            if sorted_x_term[i][1] > -1000:
                                spacer += " "
                            if sorted_x_term[i][1] > -100:
                                spacer += " "
                            if sorted_x_term[i][1] > -10:
                                spacer += " "
                        if app.ABSTENTIONS[sorted_x_term[i][0]] < 5:
                            spacer_ast = "\033[1;92m"
                        elif app.ABSTENTIONS[sorted_x_term[i][0]] == 5:
                            spacer_ast = "\033[1;93m"
                        else:
                            spacer_ast = "\033[1;91m"
                        if app.ABSTENTIONS[sorted_x_term[i][0]] < 10:
                            spacer_ast += " "

                        if app.BATTERY_STATUS[sorted_x_term[i][0]] >= 200:
                            battery_level = int(app.BATTERY_STATUS[sorted_x_term[i][0]]) - 200
                            is_charging = True
                        else:
                            battery_level = app.BATTERY_STATUS[sorted_x_term[i][0]]
                            is_charging = False

                        if battery_level == 100:
                            batStr = "\033[1;94m" + str(battery_level)
                        elif battery_level >= 50:
                            batStr = "\033[1;92m " + str(battery_level)
                        elif battery_level >= 20:
                            batStr = "\033[1;93m " + str(battery_level)
                        elif battery_level >= 10:
                            batStr = "\033[1;91m " + str(battery_level)
                        elif is_charging:
                            batStr = "\033[1;91m  " + str(battery_level)
                        elif battery_level >= 0:
                            batStr = "\033[1;91m\033[5m  " + str(battery_level)
                        else:
                            batStr = "\033[38;5;238mN/A"

                        if is_charging:
                            batStr += u"\u26a1"

                        separator = ''
                        for k in range(26-len(app.dictIDName[sorted_x_term[i][0]].decode('utf-8'))):
                            separator += ' '

                        print spacer + str(sorted_x_term[i][1]) + "\033[1;97m " + str(app.dictIDName[sorted_x_term[i][0]]) + separator + spacer_ast + str(app.ABSTENTIONS[sorted_x_term[i][0]]) + "\t" + batStr + "\033[25m"
                    print "\033[0m\n"
                #-----------------------------------------------------------
                if app.SEC_CNT+1 == len(app.SECTIONS):
                    app.load_screen('LastScreen')
                else:
                    app.load_screen("ScoreGenFinScreen")
            else:
                app.QST_PAR_CNT += 1
                app.load_screen("BeforeQstSlides")
        else:
            self.counter +=1

        app.do_backup()
