from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty

app = App.get_running_app()

class BeforeQstSlides(Screen):

    slide_img = ObjectProperty(None)
    domanda_label = ObjectProperty(None)
    counter = NumericProperty(0)

    next_button = ObjectProperty()

    Builder.load_string("""
<BeforeQstSlides>:

    name: 'BeforeQstSlides'

    next_button: next_tmp

	StackLayout:
		orientation: 'lr-tb'

		Button:
			id: domanda_label
			disabled: True
			size_hint: 0.5, 1.0/12
            text: "Domanda #"+app.QST_DSP_CNT
			text_size: self.size
			valign: 'middle'
			halign: 'center'
			font_size: 30*app.scalatore
			background_disabled_normal:''
			background_color: 0,0,0,0
			disabled_color: 1,1,1,1
			bold:True

		Button:
            id: next_tmp
			size_hint: 0.5, 1.0/12
			text: "Prosegui"
			text_size: self.size
			valign: 'middle'
			halign: 'center'
			font_size: 30*app.scalatore
			on_press: root.next()

		Button:
			id: slide_img
            size_hint: 1, 11.0/12
            disabled: True
            background_disabled_down: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_bf'][root.counter]
            background_disabled_normal: app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_bf'][root.counter]
    """)

    def on_enter(self):
        self.counter = 0
        if app.QST_DSP_CNT == '':
            if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
                app.QST_DSP_CNT = "P"
            else:
                app.QST_DSP_CNT = "1"
        # initialize the section dictionary for collection of sct scores
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            if app.SECTION_SCORE.has_key(app.SEC_CNT):
                pass
            else:
                app.SECTION_SCORE[app.SEC_CNT] = dict(zip(app.dictIDName.keys(),[0]*len(app.dictIDName.keys())))

    def next(self):
        if self.counter+1 == len(app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['img_bf']):
            app.qst_done = False
            self.counter = 0
            app.load_screen("Question")
        else:
            self.counter +=1
