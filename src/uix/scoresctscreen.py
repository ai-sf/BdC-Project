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
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

import time
import operator

app = App.get_running_app()

class IconButton(ButtonBehavior, Image):
    pass

class ScoreSctScreen(Screen):

    Builder.load_string("""
<ScoreSctScreen>:
    name : 'ScoreSctScreen'
    """)

    back_button = Button()
    back_button.bind(on_press=lambda x : app.load_screen("AfterQstSlides"))

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

        while len(sorted_x_sct) < 5:
            sorted_x_sct.append(('5355053550', -9999999))

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
        width_sep = ((1-width_icon*2)/2)*0.07
        width_pos = ((1-width_icon*2)/2)*0.10
        width_name = ((1-width_icon*2)/2)*0.5
        width_score = ((1-width_icon*2)/2)*0.33

        rows_dict = dict(zip(range(len(list1)), [row_height]*len(list1)))
        rows_dict[len(list1)] = bar_height
        g = GridLayout(cols=9,rows_minimum=rows_dict)

        pos_show=0
        list_of_pos = []
        score_prev=-123456789;

        for pos_list in range(0,len(sorted_x)):
            if sorted_x[pos_list][0] == '5355053550':
                pass
            elif sorted_x[pos_list][1] != score_prev:
                pos_show = pos_show + 1
                score_prev = sorted_x[pos_list][1]
                list_of_pos.append(pos_list+1)
            else:
                list_of_pos.append(pos_show)

        index_line = 0

        for [sx,dx] in listrighe:
            index_line = index_line + 1

            if index_line%2==1:
                line_color=[0.6,0,0.6,1]
            else:
                line_color=[0.4,0,0.4,1]

            if sx[0] == '5355053550':
                ICONsx = Button(disabled=True, size_hint_x=width_icon, background_disabled_normal='', background_color=[0,0,0,0])
                POSsx = Button(disabled=True, size_hint_x=width_pos, background_disabled_normal='', background_color=[0,0,0,0])
                NAMEsx = Button(disabled=True, size_hint_x=width_name, background_disabled_normal='', background_color=[0,0,0,0])
                SCOREsx = Button(disabled=True, size_hint_x=width_score, background_disabled_normal='', background_color=[0,0,0,0])
            else:
                ICONsx = Button(disabled=True,
                                background_normal=app.icons_path+app.dictIDicona[sx[0]],
                                background_down=app.icons_path+app.dictIDicona[sx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[sx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[sx[0]],
                                size_hint_x=width_icon, border=[0,0,0,0])

                POSsx = Button(disabled=True,
                                halign='center',
                                size_hint_x=width_pos,
                                background_color=line_color,
                                font_size=50*app.scalatore,
                                markup=True,
                                text="[color=#ff00ff][b]"+str(list_of_pos[index_line-1])+"[/b][/color]"
                                )

                name = app.dictIDName[sx[0]].decode('utf-8').split()
                try:
                    textstr_sx = name[0]+app.sep_name+name[1]+" "+name[2]
                except:
                    textstr_sx = name[0]+app.sep_name+name[1]
                num_win = len(app.SCT_FIRST_NAMES)
                if sx[0] in app.SCT_FIRST_NAMES:
                    points = str(app.PRIZE/num_win)
                    NAMEsx = Button(text="[color=#6666cc]"+textstr_sx+'\n'+"[b]+"+points+"[/b][/color]", markup=True, halign='center',disabled=True, background_disabled_normal='',
                                    background_color=line_color, color=[0.5,0.5,0.5,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                    font_name='UbuntuMono-B.ttf')
                else:
                    NAMEsx = Button(text=textstr_sx, halign='center',disabled=True, background_disabled_normal='',
                                    background_color=line_color, color=[1,1,1,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                    font_name='UbuntuMono-B.ttf')

                SCOREsx = Button(text=str(int(sx[1])), disabled=True,  background_disabled_normal='', background_color=line_color,
                                bold=True, font_size = 35*app.scalatore,size_hint_x=width_score)

            sep = Button(disabled=True,
                        background_disabled_normal='',
                        background_normal='',
                        background_color=[0,0,0,1],
                        size_hint_x=width_sep)

            if dx[0] == '5355053550':
                ICONdx = Button(disabled=True, size_hint_x=width_icon, background_disabled_normal='', background_color=[0,0,0,0])
                POSdx = Button(disabled=True, size_hint_x=width_pos, background_disabled_normal='', background_color=[0,0,0,0])
                NAMEdx = Button(disabled=True, size_hint_x=width_name, background_disabled_normal='', background_color=[0,0,0,0])
                SCOREdx = Button(disabled=True, size_hint_x=width_score, background_disabled_normal='', background_color=[0,0,0,0])
            else:
                ICONdx = Button(disabled=True, size_hint_x=width_icon, border=[0,0,0,0],
                                background_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_down=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[dx[0]] )

                POSdx = Button(disabled=True,
                                halign='center',
                                size_hint_x=width_pos,
                                background_color=line_color,
                                font_size=50*app.scalatore,
                                markup=True,
                                text="[color=#ff00ff][b]"+str(list_of_pos[index_line+len(list1)-1])+"[/b][/color]"
                                )

                name = app.dictIDName[dx[0]].decode('utf-8').split()
                try:
                    textstr_dx = name[0]+app.sep_name+name[1]+" "+name[2]
                except:
                    textstr_dx = name[0]+app.sep_name+name[1]
                if dx[0] in app.SCT_FIRST_NAMES:
                    points = str(app.PRIZE/num_win)
                    NAMEdx = Button(text="[color=#6666cc]"+textstr_dx+'\n'+"[b]+"+points+"[/b][/color]", markup=True, halign='center',disabled=True, background_disabled_normal='',
                                    background_color=line_color, color=[0.5,0.5,0.5,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                    font_name='UbuntuMono-B.ttf')
                else:
                    NAMEdx = Button(text=textstr_dx, halign='center',disabled=True, background_disabled_normal='',
                                    background_color=line_color, color=[1,1,1,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                    font_name='UbuntuMono-B.ttf')
                SCOREdx = Button(text=str(int(dx[1])), disabled=True,background_disabled_normal='', background_color=line_color, bold=True,
                                 font_size = 35*app.scalatore,size_hint_x=width_score)

            g.add_widget(POSsx)
            g.add_widget(ICONsx)
            g.add_widget(NAMEsx)
            g.add_widget(SCOREsx)
            g.add_widget(sep)
            g.add_widget(POSdx)
            g.add_widget(ICONdx)
            g.add_widget(NAMEdx)
            g.add_widget(SCOREdx)

        lBACK = Button(text="%s"%(iconfonts.icon('fa-backward')),font_size=50*app.scalatore,bold=True, halign='center', size_hint_x=width_icon, markup=True)
        lBACK.bind(on_press=lambda x : app.load_screen("AfterQstSlides"))

        bmsx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCsx= Button(disabled=True, background_disabled_normal='',  background_color=[0,0,0,0], size_hint_x=width_score)

        separation = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_sep)

        separation2 = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_pos)
        separation3 = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_pos)

        bmdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_icon)

        bottomdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCdx = IconButton(source='img/logoBdC_bianco.png', size_hint_x=width_score)
        iconBDCdx.bind(on_press=lambda x : app.cmd_line_start())

        g.add_widget(separation2)
        g.add_widget(lBACK)
        g.add_widget(bmsx)
        g.add_widget(iconBDCsx)
        g.add_widget(separation)
        g.add_widget(separation3)
        g.add_widget(bmdx)
        g.add_widget(bottomdx)
        g.add_widget(iconBDCdx)

        self.add_widget(g)
