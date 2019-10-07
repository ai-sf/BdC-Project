from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

class BDCScreenManager(ScreenManager):

    Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition

<BDCScreenManager>
    transition: NoTransition()
    """)
