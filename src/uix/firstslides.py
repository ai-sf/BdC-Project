from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty

app = App.get_running_app()

class FirstSlides(Screen):

    slide_img = ObjectProperty(None)
    domanda_label = ObjectProperty(None)
    counter = NumericProperty(0)

    next_button = ObjectProperty()

    Builder.load_string("""
<FirstSlides>:

    name: 'FirstSlides'
    next_button: next

	StackLayout:
		orientation: 'lr-tb'

		Button:
			id: domanda_label
			disabled: True
			size_hint: 0.5, 1.0/12
			text: "Welcome to BdC!"
			text_size: self.size
			valign: 'center'
			halign: 'center'
			font_size: 30*app.scalatore
			background_color: 0,0,0,0
			disabled_color: 1,1,1,1
			bold:True

		Button:
            id: next
			size_hint: 0.5, 1.0/12
			text: "Prosegui"
			text_size: self.size
			valign: 'center'
			halign: 'center'
			font_size: 30*app.scalatore
			on_press: root.next()

		Button:
			id: slide_img
			size_hint: 1, 11.0/12
			disabled: True
            background_disabled_normal: app.FIRST_SLIDES[root.counter]
            background_disabled_down: app.FIRST_SLIDES[root.counter]
    """)


    def on_enter(self):
        if not app.FIRST_SLIDES:
            app.load_screen('BeforeQstSlides')

    def next(self):
        if self.counter+1 == len(app.FIRST_SLIDES):
            app.load_screen('BeforeQstSlides')
        else:
            self.counter +=1
