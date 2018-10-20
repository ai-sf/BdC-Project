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

import operator

app = App.get_running_app()

class ScoreQstScreen(Screen):

    Builder.load_string("""
<ScoreQstScreen>:
    name : 'ScoreQstScreen'
    """)

    def on_enter(self):

        if app.score_qst_ready == True:
            pass
        else:
            self.clear_widgets()
            self.Score = [(key, app.QUESTION_SCORE[-1][key][0]) for key in app.QUESTION_SCORE[-1].keys()]
            sorted_x = sorted(self.Score, key=operator.itemgetter(1), reverse= True)

            # if odd, add a fake name
            if len(sorted_x) % 2 == 1:
                sorted_x.append(('5355053550', -9999999))

            self.buildClassifica(sorted_x)

    def buildClassifica(self, sorted_x):

        list1 = sorted_x[:len(sorted_x)/2]
        list2 = sorted_x[len(sorted_x)/2:]
        listrighe = [[list1[i],list2[i]] for i in range(len(sorted_x)/2)]

        bar_height = float(Window.height)*0.1
        row_height = (float(Window.height)-bar_height)/(float(len(sorted_x))/2)
        width_icon = row_height/Window.width
        width_sep = 1.0/100
        width_name = (((1-width_icon*2)-width_sep)/2)*0.65
        width_score = (((1-width_icon*2)-width_sep)/2)*0.35

        rows_dict = dict(zip(range(len(listrighe)), [row_height]*len(listrighe)))
        rows_dict[len(listrighe)] = bar_height
        g = GridLayout(id='grid',cols=7,rows_minimum=rows_dict)

        for [sx,dx] in listrighe:

            ICONsx = Button(disabled=True,
                            background_normal=app.icons_path+app.dictIDicona[sx[0]],
                            background_down=app.icons_path+app.dictIDicona[sx[0]],
                            background_disabled_normal=app.icons_path+app.dictIDicona[sx[0]],
                            background_disabled_down=app.icons_path+app.dictIDicona[sx[0]],
                            size_hint_x=width_icon, border=[0,0,0,0])


            name = app.dictIDName[sx[0]].split()
            NAMEsx = Button(text=name[0]+'\n'+name[1],
                            halign='center',
                            disabled=True,
                            background_disabled_normal='',
                            background_color=[0,0,0,0],
                            color=[1,1,1,1],
                            font_size=40*app.scalatore,
                            size_hint_x = width_name,
                            font_name='font/UbuntuMono-B.ttf')

            if int(sx[1]) > 0:
                colore = [0,0.8,0,1]
                colorehtml = '#00cc00'
                timesx = str("{0:.2f}".format(round(app.QUESTION_SCORE[-1][str(sx[0])][1],2)))+"\'\'"
            if int(sx[1]) == 0:
                colore = [1,0.75,0.095,1]
                colorehtml = '#ffcc00'
                timesx = '-'
            if int(sx[1]) < 0:
                colore = [0.8,0,0,1]
                colorehtml = '#ff0000'
                if app.QUESTION_SCORE[-1][str(sx[0])][1] is None:
                    timesx = '-'
                else:
                    timesx = str("{0:.2f}".format(round(app.QUESTION_SCORE[-1][str(sx[0])][1],2)))+"\'\'"

            scoresx_string = '[size='+str(int(45*app.scalatore))+'][color='+colorehtml+'][b]'+str(int(sx[1]))+'[/b][/size][size='+str(int(30*app.scalatore))+']\n'+timesx+'[/color][/size]'
            SCOREsx = Button(text=scoresx_string, disabled=True, background_disabled_normal='',
                            background_color=[0,0,0,0],markup=True,
                            font_size = 35*app.scalatore,size_hint_x=width_score,halign='center')

            sep = Button(disabled=True, background_disabled_normal='', background_color=[1,1,1,1],size_hint_x=width_sep)

            if dx[0] == '5355053550':
                ICONdx = Button(disabled=True, size_hint_x=width_icon, background_disabled_normal='', background_color=[0,0,0,0])
                NAMEdx = Button(disabled=True, size_hint_x=width_name, background_disabled_normal='', background_color=[0,0,0,0])
                SCOREdx = Button(disabled=True, size_hint_x=width_score, background_disabled_normal='', background_color=[0,0,0,0])
            else:
                ICONdx = Button(disabled=True, size_hint_x=width_icon,
                                background_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_down=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[dx[0]],
                                border=[0,0,0,0])

                name = app.dictIDName[dx[0]].split()
                NAMEdx = Button(text=name[0]+'\n'+name[1], halign='center', disabled=True, background_disabled_normal='',
                                background_color=[0,0,0,0], disabled_color=[1,1,1,1], font_size=40*app.scalatore,size_hint_x=width_name,
                                font_name='font/UbuntuMono-B.ttf')

                if int(dx[1]) > 0:
                    colore = [0,0.8,0,1]
                    colorehtml = '#00cc00'
                    timedx = str("{0:.2f}".format(round(app.QUESTION_SCORE[-1][str(dx[0])][1],2)))+"\'\'"
                if int(dx[1]) == 0:
                    colore = [1,0.75,0.095,1]
                    colorehtml = '#ffcc00'
                    timedx = '-'
                if int(dx[1]) < 0:
                    colore = [0.8,0,0,1]
                    colorehtml = '#ff0000'
                    if app.QUESTION_SCORE[-1][str(dx[0])][1] is None:
                        timedx = '-'
                    else:
                        timedx = str("{0:.2f}".format(round(app.QUESTION_SCORE[-1][str(dx[0])][1],2)))+"\'\'"


                scoredx_string = '[size='+str(int(45*app.scalatore))+'][color='+colorehtml+'][b]'+str(int(dx[1]))+'[/b][/size][size='+str(int(30*app.scalatore))+']\n'+timedx+'[/color][/size]'
                SCOREdx = Button(text=scoredx_string, disabled=True, background_disabled_normal='', background_color=[0,0,0,0], markup=True,
                                 font_size = 35*app.scalatore,size_hint_x=width_score,halign='center')

            g.add_widget(ICONsx)
            g.add_widget(NAMEsx)
            g.add_widget(SCOREsx)
            g.add_widget(sep)
            g.add_widget(ICONdx)
            g.add_widget(NAMEdx)
            g.add_widget(SCOREdx)

        lBACK = Button(id='back_tmp', text='back',font_size=30*app.scalatore,bold=True, halign='center', size_hint_x=width_icon)
        lBACK.bind(on_press=lambda x : app.load_screen("Question"))
        bmsx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCsx= Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0], size_hint_x=width_score)

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
#        g.add_widget(ObjectProperty('back_tmp'),)

        self.add_widget(g)
#        self.add_widget(back_button=ObjectProperty('back_button_tmp'))
        app.score_qst_ready = True
