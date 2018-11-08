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

import sys
sys.path.insert(0, app.main_path)

class ScoreGenFinScreen(Screen):

    Builder.load_string("""
<ScoreGenFinScreen>:
    name : 'ScoreGenFinScreen'
    """)

    def on_enter(self):
        self.clear_widgets()

        #reset classifica dopo sezione di prova
        if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            app.GENERAL_SCORE = app.dictIDReset
            app.score_new = True

        app.Score = [(key, app.GENERAL_SCORE[key]) for key in app.GENERAL_SCORE.keys()]
        app.sorted_x = sorted(app.Score, key=operator.itemgetter(1), reverse= True)
        if app.Position:
            app.PositionBefore = app.Position
        app.Position = {}
        for name in app.dictIDName.keys():
            app.Position[name] = [j[0] for j in app.sorted_x].index(name)

        self.Score = app.Score
        self.Position = app.Position
        self.PositionBefore = app.PositionBefore

        app.newPositionBefore = True

        sorted_x = app.sorted_x

        #print classifica iniziale a terminale dopo sezione di test
        if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
            print "\033[1;97m\033[1;100m"
            print "CLASSIFICA INIZIALE ----------------------------\n"
            for i in range(len(sorted_x)):
                spacer = "\033[1;96m"
                if sorted_x[i][1] >= 0:
                    if sorted_x[i][1] < 10000:
                        spacer += " "
                    if sorted_x[i][1] < 1000:
                        spacer += " "
                    if sorted_x[i][1] < 100:
                        spacer += " "
                    if sorted_x[i][1] < 10:
                        spacer += " "
                else:
                    if sorted_x[i][1] > -1000:
                        spacer += " "
                    if sorted_x[i][1] > -100:
                        spacer += " "
                    if sorted_x[i][1] > -10:
                        spacer += " "

                print spacer + str(sorted_x[i][1]) + "\033[1;97m " + str(app.dictIDName[sorted_x[i][0]])
            print "\033[0m\n"

        while len(sorted_x) < 5:
            sorted_x.append(('5355053550', -9999999))

        # if odd, add a fake name
        if len(sorted_x) % 2 == 1:
            sorted_x.append(('5355053550', -9999999))

        self.buildClassifica(sorted_x)

    def next(self):
        if app.SEC_CNT+1 == len(app.SECTIONS):
            pass
        else:
            app.SEC_CNT += 1

            if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
                app.QST_NOR_CNT += 1
                app.QST_DSP_CNT = str(app.QST_NOR_CNT)
            if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
                app.QST_NOR_CNT += 1
                app.QST_DSP_CNT = str(app.QST_NOR_CNT)
            if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
                app.QST_DSP_CNT = "P"
            if app.SECTIONS[app.SEC_CNT]['type'] == 'normal':
                app.load_screen("BeforeQstSlides")
            if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
                app.load_screen("BeforeQstSlides")
            if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
                app.load_screen("IntroSctScreen")

    def buildClassifica(self, sorted_x):

        list1 = sorted_x[:len(sorted_x)/2]
        list2 = sorted_x[len(sorted_x)/2:]
        listrighe = [[list1[i],list2[i]] for i in range(len(sorted_x)/2)]

        bar_height = float(Window.height)*0.1
        row_height = (float(Window.height)-bar_height)/(float(len(sorted_x))/2)
        width_icon = row_height/Window.width
        # width_arrow = width_icon*0.75
        width_arrow = width_icon*0.25
        width_sep = 1.0/50
        width_name = ((1-width_icon*2-width_arrow*2-width_sep)/2)*(1.75/3)
        width_score = ((1-width_icon*2-width_arrow*2-width_sep)/2)*(1.25/3)

        rows_dict = dict(zip(range(len(list1)), [row_height]*len(list1)))
        rows_dict[len(list1)] = bar_height
        g = GridLayout(cols=9,#row_default_height=row_height,row_force_default=True,
                       rows_minimum=rows_dict)

        app.score_seen = True

        for [sx,dx] in listrighe:
            if sx[0] == '5355053550':
                ICONsx = Button(disabled=True, size_hint_x=width_icon, background_disabled_normal='', background_color=[0,0,0,0])
                ARROWsx = Button(disabled=True, size_hint_x=width_arrow, background_disabled_normal='', background_color=[0,0,0,0])
                NAMEsx = Button(disabled=True, size_hint_x=width_name, background_disabled_normal='', background_color=[0,0,0,0])
                SCOREsx = Button(disabled=True, size_hint_x=width_score, background_disabled_normal='', background_color=[0,0,0,0])
            else:
                ICONsx = Button(disabled=True,
                                background_normal=app.icons_path+app.dictIDicona[sx[0]],
                                background_down=app.icons_path+app.dictIDicona[sx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[sx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[sx[0]],
                                size_hint_x=width_icon, border=[0,0,0,0])

                if app.score_new:
                    if sx[1] > 0:
                        #arrow = 'img/arrow_green.png'
                        arrow = 'fa-arrow-up'
                        arrow_color = '#00cc00'
                    elif sx[1] == 0:
                        #arrow = 'img/arrow_yellow.png'
                        arrow = 'fa-minus'
                        arrow_color = '#ffcc00'
                    elif sx[1] < 0:
                        #arrow = 'img/arrow_red.png'
                        arrow = 'fa-arrow-down'
                        arrow_color = '#ff0000'
                else:
                    if self.Position[sx[0]] < self.PositionBefore[sx[0]]:
                        #arrow = 'img/arrow_green.png'
                        arrow = 'fa-arrow-up'
                        arrow_color = '#00cc00'
                    if self.Position[sx[0]] == self.PositionBefore[sx[0]]:
                        #arrow = 'img/arrow_yellow.png'
                        arrow = 'fa-minus'
                        arrow_color = '#ffcc00'
                    if self.Position[sx[0]] > self.PositionBefore[sx[0]]:
                        #arrow = 'img/arrow_red.png'
                        arrow = 'fa-arrow-down'
                        arrow_color = '#ff0000'

                # ARROWsx = Button(disabled=True,
                #                 background_normal=arrow,
                #                 background_down=arrow,
                #                 background_disabled_normal=arrow,
                #                 background_disabled_down=arrow,
                #                 size_hint_x=width_arrow)

                ARROWsx = Button(disabled=True,
                                size_hint_x=width_arrow,
                                background_color=[0,0,0,0],
                                font_size=50*app.scalatore,
                                markup=True,
                                text="[color="+arrow_color+"]%s[/color] "%(iconfonts.icon(arrow))
                                )

                name = app.dictIDName[sx[0]].split()
                textstr_sx = name[0]+'\n'+name[1]
                if sx[0] in app.WINNER_OF_SECTIONS.keys():
                    textstr_sx += '\n'
                    for ic in app.WINNER_OF_SECTIONS[sx[0]]:
                        textstr_sx += " [color=#6666cc]%s[/color] "%(iconfonts.icon(ic))

                NAMEsx = Button(text=textstr_sx, markup=True, halign='center',disabled=True, background_disabled_normal='',
                                background_color=[0,0,0,0], color=[1,1,1,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                font_name='UbuntuMono-B.ttf')
                SCOREsx = Button(text=str(int(sx[1])), disabled=True,  background_disabled_normal='', background_color=[0,0,0,0],
                                bold=True, font_size = 35*app.scalatore,size_hint_x=width_score)

            sep = Button(disabled=True, background_disabled_normal='', background_color=[1,1,1,1],size_hint_x=width_sep)

            if dx[0] == '5355053550':
                ICONdx = Button(disabled=True, size_hint_x=width_icon, background_disabled_normal='', background_color=[0,0,0,0])
                ARROWdx = Button(disabled=True, size_hint_x=width_arrow, background_disabled_normal='', background_color=[0,0,0,0])
                NAMEdx = Button(disabled=True, size_hint_x=width_name, background_disabled_normal='', background_color=[0,0,0,0])
                SCOREdx = Button(disabled=True, size_hint_x=width_score, background_disabled_normal='', background_color=[0,0,0,0])
            else:
                ICONdx = Button(disabled=True, size_hint_x=width_icon, border=[0,0,0,0],
                                background_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_down=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[dx[0]] )

                if app.score_new:
                    if dx[1] > 0:
                        #arrow = 'img/arrow_green.png'
                        arrow = 'fa-arrow-up'
                        arrow_color = '#00cc00'
                    elif dx[1] == 0:
                        #arrow = 'img/arrow_yellow.png'
                        arrow = 'fa-minus'
                        arrow_color = '#ffcc00'
                    elif dx[1] < 0:
                        #arrow = 'img/arrow_red.png'
                        arrow = 'fa-arrow-down'
                        arrow_color = '#ff0000'
                else:
                    if self.Position[dx[0]] < self.PositionBefore[dx[0]]:
                        #arrow = 'img/arrow_green.png'
                        arrow = 'fa-arrow-up'
                        arrow_color = '#00cc00'
                    if self.Position[dx[0]] == self.PositionBefore[dx[0]]:
                        #arrow = 'img/arrow_yellow.png'
                        arrow = 'fa-minus'
                        arrow_color = '#ffcc00'
                    if self.Position[dx[0]] > self.PositionBefore[dx[0]]:
                        #arrow = 'img/arrow_red.png'
                        arrow = 'fa-arrow-down'
                        arrow_color = '#ff0000'

                # ARROWdx = Button(disabled=True,
                #                 background_normal=arrow,
                #                 background_down=arrow,
                #                 background_disabled_normal=arrow,
                #                 background_disabled_down=arrow,
                #                 size_hint_x=width_arrow)

                ARROWdx = Button(disabled=True,
                                size_hint_x=width_arrow,
                                background_color=[0,0,0,0],
                                font_size=50*app.scalatore,
                                markup=True,
                                text="[color="+arrow_color+"]%s[/color] "%(iconfonts.icon(arrow))
                                )

                name = app.dictIDName[dx[0]].split()
                textstr_dx = name[0]+'\n'+name[1]
                if dx[0] in app.WINNER_OF_SECTIONS.keys():
                    textstr_dx += '\n'
                    for ic in app.WINNER_OF_SECTIONS[dx[0]]:
                        textstr_dx += " [color=#6666cc]%s[/color] "%(iconfonts.icon(ic))

                NAMEdx = Button(text=textstr_dx, markup=True, halign='center',disabled=True, background_disabled_normal='',
                                background_color=[0,0,0,0], color=[1,1,1,1], font_size=35*app.scalatore, size_hint_x = width_name,
                                font_name='UbuntuMono-B.ttf')
                SCOREdx = Button(text=str(int(dx[1])), disabled=True,background_disabled_normal='', background_color=[0,0,0,0], bold=True,
                                 font_size = 35*app.scalatore,size_hint_x=width_score)

            g.add_widget(ICONsx)
            g.add_widget(ARROWsx)
            g.add_widget(NAMEsx)
            g.add_widget(SCOREsx)
            g.add_widget(sep)
            g.add_widget(ICONdx)
            g.add_widget(ARROWdx)
            g.add_widget(NAMEdx)
            g.add_widget(SCOREdx)


        app.score_new = False

        lBACK = Button(text="%s"%(iconfonts.icon('fa-forward')),font_size=50*app.scalatore,bold=True, halign='center', size_hint_x=width_icon, markup=True)
        lBACK.bind(on_press= lambda x : self.next())

        absx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_arrow)

        bmsx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCsx= Button(disabled=True, background_disabled_normal='',  background_color=[0,0,0,0], size_hint_x=width_score)

        separation = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_sep)

        bmdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_icon)
        abdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_arrow)

        bottomdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCdx = Button(disabled=False, background_disabled_down='img/logoBdC_bianco.png',
                        background_disabled_normal='img/logoBdC_bianco.png',background_down='img/logoBdC_bianco.png',
                        background_normal='img/logoBdC_bianco.png', background_color=[1,1,1,1], size_hint_x=width_score)
        iconBDCdx.bind(on_press=lambda x : app.cmd_line_start())

        g.add_widget(lBACK)
        g.add_widget(absx)
        g.add_widget(bmsx)
        g.add_widget(iconBDCsx)
        g.add_widget(separation)
        g.add_widget(bmdx)
        g.add_widget(abdx)
        g.add_widget(bottomdx)
        g.add_widget(iconBDCdx)

        self.add_widget(g)
