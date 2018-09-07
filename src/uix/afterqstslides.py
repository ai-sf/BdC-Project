from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty

app = App.get_running_app()

class AfterQstSlides(Screen):

    label_score = StringProperty('')
    slide_img = ObjectProperty(None)
    counter = NumericProperty(0)

    showScoreGen = BooleanProperty(True)

    next_button = ObjectProperty()
    score_button = ObjectProperty()
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
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            self.label_score = 'CLASSIFICA SEZIONE'
        if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
            self.label_score = 'CLASSIFICA GENERALE'
        if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            self.label_score = 'CLASSIFICA GENERALE'

    def show_score(self):
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            app.load_screen('ScoreSecScreen')
        if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
            app.load_screen('ScoreGenScreen')
        if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            app.load_screen('ScoreGenScreen')

    def next(self):
        if self.counter+1 == len(app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_af']):
            if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
                app.QST_DSP_CNT = str(int(app.QST_DSP_CNT)+1)
                app.QST_NOR_CNT += 1
            app.QST_TOT_CNT += 1
            if app.QST_PAR_CNT+1 == len(app.QUESTIONS[app.SEC_CNT]):
                app.QST_PAR_CNT = 0
                if app.SEC_CNT+1 == len(app.QUESTIONS):
                    app.load_screen('LastScreen')
                else:
                    app.SEC_CNT += 1
                    if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
                        app.QST_DSP_CNT = str(app.QST_NOR_CNT)
                    if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
                        app.QST_DSP_CNT = "P"
                    app.load_screen("BeforeQstSlides")
            else:
                app.QST_PAR_CNT += 1
                app.load_screen("BeforeQstSlides")
        else:
            self.counter +=1
