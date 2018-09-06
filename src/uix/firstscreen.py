from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty

app = App.get_running_app()

class FirstScreen(Screen):

    next_button = ObjectProperty()

    Builder.load_string("""
<FirstScreen>:

    name: 'FirstScreen'
    next_button: next

    BackImage:
        orientation: 'rl-tb'
        Button:
            id: next
            size_hint: (0.25*709/1063)*16/9, 0.25
        	text: "INIZIA GIOCO"
        	text_size: self.size
        	valign: 'middle'
        	halign: 'center'
        	on_press: app.load_screen('FirstSlides')
        	font_size: 30*app.scalatore
        	background_normal: 'img/logo_AISF.png'
        	bold:True
        	background_color: 1,1,1,0.5
    """)

class BackImage(StackLayout):

    Builder.load_string("""
<BackImage>:
	canvas.before:
		BorderImage:
			border: 10, 10, 10, 10
			source: 'img/logoBdC_bianco.png'
			pos: self.pos
			size: self.size
    """)
