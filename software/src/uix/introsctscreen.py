from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty

app = App.get_running_app()

class IntroSctScreen(Screen):

    next_button = ObjectProperty()

    Builder.load_string("""
<IntroSctScreen>:

    name: 'IntroSctScreen'
    next_button: next_tmp

	StackLayout:
		orientation: 'lr-tb'

		Button:
            id: next_tmp
			size_hint: 1.0, 1.0/12
			text: "Sezione: "+app.SECTIONS[app.SEC_CNT]['name'].upper()
			text_size: self.size
			valign: 'middle'
			halign: 'center'
			font_size: 30*app.scalatore
			on_press: app.load_screen('BeforeQstSlides')

		Button:
			id: slide_img
			size_hint: 1, 11.0/12
			disabled: True
            background_disabled_down: app.SECTIONS[app.SEC_CNT]['intro']
            background_disabled_normal: app.SECTIONS[app.SEC_CNT]['intro']
    """)

    def on_enter(self):
        print(app.SECTIONS[app.SEC_CNT]['bkg'])
