from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty

app = App.get_running_app()

class LastScreen(Screen):

    counter = NumericProperty(int(app.NUMERO_GIOCATORI-1))

    Builder.load_string("""
<LastScreen>:

    name: 'LastScreen'

	FloatLayout:
		Button:
			size_hint: 0.5*root.height/root.width, 0.5
			pos_hint: {'center_x':0.5, 'center_y':0.7}
			disabled: True
			background_disabled_normal: app.icons_path+app.dictIDicona[app.sorted_x[root.counter][0]]
		Label:
			pos_hint: {'center_x':0.5, 'center_y': 0.35}
			text: str(root.counter+1)+' - '+app.dictIDName[app.sorted_x[root.counter][0]]
			text_size: self.size
			font_size: 80*app.scalatore
			bold:True
			valign: 'center'
			halign: 'center'
			font_name: 'font/Ubuntu-L.ttf'
			color: 1,1,1,1
			markup: True
		Label:
			pos_hint: {'center_x':0.5, 'center_y': 0.2}
			text: str(app.GENERAL_SCORE[app.sorted_x[root.counter][0]])
			text_size: self.size
			font_size: 150*app.scalatore
			bold:True
			valign: 'center'
			halign: 'center'
			font_name: 'font/Cratense.ttf'
			color: 1,1,1,1
			markup: True
		Button:
			size_hint: 0.2, 0.2
			pos_hint: {'center_x': 0.9, 'center_y': 0.1}
			text: 'next'
			background_normal: 'img/button_white.png'
			font_size: 40*app.scalatore
			on_press: root.nextpos()
		Button:
            disabled: True if (root.counter == app.NUMERO_GIOCATORI-1) else False
			size_hint: 0.2, 0.2
			pos_hint: {'center_x': 0.1, 'center_y': 0.1}
			text: 'back'
			background_normal: 'img/button_white.png'
			font_size: 40*app.scalatore
			on_press: root.backpos()
    """)


    def nextpos(self):

        if self.counter > 0:
            self.counter -= 1
        else:
            pass

    def backpos(self):

        self.counter += 1
