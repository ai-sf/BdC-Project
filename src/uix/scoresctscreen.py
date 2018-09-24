from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window

import iconfonts.iconfonts as iconfonts

import time
import operator


app = App.get_running_app()

class ScoreSctScreen(Screen):

    Builder.load_string("""
<ScoreSctScreen>:
    name : 'ScoreSctScreen'
    """)

    def on_enter(self):
        self.clear_widgets()
        self.Score = app.Score_sct

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

        sorted_x_sct = app.sorted_x_sct
        # if odd, add a fake name
        if len(sorted_x_sct) % 2 == 1:
            sorted_x_sct.append(('5355053550', -9999999))

        self.buildClassifica(sorted_x_sct)

    def buildClassifica(self, sorted_x):

        list1 = sorted_x[:len(sorted_x)/2]
        list2 = sorted_x[len(sorted_x)/2:]
        listrighe = [[list1[i],list2[i]] for i in range(len(sorted_x)/2)]

        bar_height = float(Window.height)*0.1
        row_height = (float(Window.height)-bar_height)/(float(len(sorted_x))/2)
        width_icon = row_height/Window.width
        # width_arrow = width_icon*0.75
        width_sep = 1.0/50
        width_name = ((1-width_icon*2-width_sep)/2)*(1.75/3)
        width_score = ((1-width_icon*2-width_sep)/2)*(1.25/3)

        rows_dict = dict(zip(range(len(list1)), [row_height]*len(list1)))
        rows_dict[len(list1)] = bar_height
        g = GridLayout(cols=7,#row_default_height=row_height,row_force_default=True,
                       rows_minimum=rows_dict)

        for [sx,dx] in listrighe:

            ICONsx = Button(disabled=True,
                            background_normal=app.icons_path+app.dictIDicona[sx[0]],
                            background_down=app.icons_path+app.dictIDicona[sx[0]],
                            background_disabled_normal=app.icons_path+app.dictIDicona[sx[0]],
                            background_disabled_down=app.icons_path+app.dictIDicona[sx[0]],
                            size_hint_x=width_icon, border=[0,0,0,0])

            name = app.dictIDName[sx[0]].split()
            num_win = len(app.SCT_FIRST_NAMES)
            if sx[0] in app.SCT_FIRST_NAMES:
                points = str(app.PRIZE/num_win)
                NAMEsx = Button(text="[color=#6666cc]"+name[0]+'\n'+name[1]+'\n'+"[b]+"+points+"[/b][/color]", markup=True, halign='center',disabled=True, background_disabled_normal='',
                                background_color=[0,0,0,0], color=[0.5,0.5,0.5,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                font_name='UbuntuMono-B.ttf')
            else:
                NAMEsx = Button(text=name[0]+'\n'+name[1], halign='center',disabled=True, background_disabled_normal='',
                                background_color=[0,0,0,0], color=[1,1,1,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                font_name='UbuntuMono-B.ttf')

            SCOREsx = Button(text=str(int(sx[1])), disabled=True,  background_disabled_normal='', background_color=[0,0,0,0],
                            bold=True, font_size = 35*app.scalatore,size_hint_x=width_score)

            sep = Button(disabled=True, background_disabled_normal='', background_color=[1,1,1,1],size_hint_x=width_sep)

            if dx[0] == '5355053550':
                ICONdx = Button(disabled=True, size_hint_x=width_icon, background_disabled_normal='', background_color=[0,0,0,0])
                NAMEdx = Button(disabled=True, size_hint_x=width_name, background_disabled_normal='', background_color=[0,0,0,0])
                SCOREdx = Button(disabled=True, size_hint_x=width_score, background_disabled_normal='', background_color=[0,0,0,0])
            else:
                ICONdx = Button(disabled=True, size_hint_x=width_icon, border=[0,0,0,0],
                                background_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_down=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[dx[0]] )

                name = app.dictIDName[dx[0]].split()
                if dx[0] in app.SCT_FIRST_NAMES:
                    points = str(app.PRIZE/num_win)
                    NAMEdx = Button(text="[color=#6666cc]"+name[0]+'\n'+name[1]+'\n'+"[b]+"+points+"[/b][/color]", markup=True, halign='center',disabled=True, background_disabled_normal='',
                                    background_color=[0,0,0,0], color=[0.5,0.5,0.5,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                    font_name='UbuntuMono-B.ttf')
                else:
                    NAMEdx = Button(text=name[0]+'\n'+name[1], halign='center',disabled=True, background_disabled_normal='',
                                    background_color=[0,0,0,0], color=[1,1,1,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                    font_name='UbuntuMono-B.ttf')
                SCOREdx = Button(text=str(int(dx[1])), disabled=True,background_disabled_normal='', background_color=[0,0,0,0], bold=True,
                                 font_size = 35*app.scalatore,size_hint_x=width_score)

            g.add_widget(ICONsx)
            g.add_widget(NAMEsx)
            g.add_widget(SCOREsx)
            g.add_widget(sep)
            g.add_widget(ICONdx)
            g.add_widget(NAMEdx)
            g.add_widget(SCOREdx)

        lBACK = Button(text='back',font_size=30*app.scalatore,bold=True, halign='center', size_hint_x=width_icon)
        lBACK.bind(on_press=lambda x : app.load_screen("AfterQstSlides"))

        bmsx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCsx= Button(disabled=True, background_disabled_normal='',  background_color=[0,0,0,0], size_hint_x=width_score)

        separation = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_sep)

        bmdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_icon)

        bottomdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCdx = Button(disabled=True, background_disabled_down='img/logoBdC_bianco.png',
                        background_disabled_normal='img/logoBdC_bianco.png',background_down='img/logoBdC_bianco.png',
                        background_normal='img/logoBdC_bianco.png', background_color=[1,1,1,1], size_hint_x=width_score)

        g.add_widget(lBACK)
        g.add_widget(bmsx)
        g.add_widget(iconBDCsx)
        g.add_widget(separation)
        g.add_widget(bmdx)
        g.add_widget(bottomdx)
        g.add_widget(iconBDCdx)

        self.add_widget(g)
