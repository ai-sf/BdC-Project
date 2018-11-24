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
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import operator

app = App.get_running_app()

class IconButton(ButtonBehavior, Image):
    pass

class ScoreQstScreen(Screen):

    Builder.load_string("""
<ScoreQstScreen>:
    name : 'ScoreQstScreen'
    """)

    back_button = Button()
    back_button.bind(on_press=lambda x : app.load_screen("Question"))

    def on_enter(self):

        if app.score_qst_ready == True:
            pass
        else:
            self.clear_widgets()
            self.Score_R = []
            self.Score_A = []
            self.Score_W = []

            for key in app.QUESTION_SCORE[-1].keys():
                if app.QUESTION_SCORE[-1][key][0] < 0:
                    if(key in app.lastRisposteDate.keys()):
                        self.Score_W.append((key, app.QUESTION_SCORE[-1][key][0], app.QUESTION_SCORE[-1][key][1], app.lastRisposteDate[key][0]))
                    else:
                        self.Score_W.append((key, app.QUESTION_SCORE[-1][key][0], app.QUESTION_SCORE[-1][key][1], '-'))
                elif app.QUESTION_SCORE[-1][key][0] > 0:
                    self.Score_R.append((key, app.QUESTION_SCORE[-1][key][0], app.QUESTION_SCORE[-1][key][1], app.lastRisposteDate[key][0]))
                else:
                    self.Score_A.append((key, app.QUESTION_SCORE[-1][key][0], app.QUESTION_SCORE[-1][key][1], '-'))

            sorted_R = sorted(self.Score_R, key=operator.itemgetter(2))
            sorted_R = sorted(sorted_R, key=operator.itemgetter(1), reverse= True)

            sorted_W = sorted(self.Score_W, key=operator.itemgetter(2), reverse=True)
            sorted_W = sorted(sorted_W, key=operator.itemgetter(1), reverse= True)

            self.sorted_x = sorted_R+self.Score_A+sorted_W

            while len(self.sorted_x) < 5:
                self.sorted_x.append(('5355053550', -9999999))

            # if odd, add a fake name
            if len(self.sorted_x) % 2 == 1:
                self.sorted_x.append(('5355053550', -9999999))

            self.letterVisibility = False
            self.buildClassifica(self.sorted_x)

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
            if sx[0] == '5355053550':
                ICONsx = Button(disabled=True, size_hint_x=width_icon, background_disabled_normal='', background_color=[0,0,0,0])
                NAMEsx = Button(disabled=True, size_hint_x=width_name, background_disabled_normal='', background_color=[0,0,0,0])
                SCOREsx = Button(disabled=True, size_hint_x=width_score, background_disabled_normal='', background_color=[0,0,0,0])
            else:
                ICONsx = Button(disabled=False,
                                text=sx[0]+","+sx[3]+","+str(sx[1]),
                                color=[0,0,0,0],
                                background_normal=app.icons_path+app.dictIDicona[sx[0]],
                                background_down=app.icons_path+app.dictIDicona[sx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[sx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[sx[0]],
                                size_hint_x=width_icon, border=[0,0,0,0])

                ICONsx.bind(on_press=self.answer_popup)

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

                if self.letterVisibility:
                    if sx[3] != '-':
                        scoresx_string = '[size='+str(int(45*app.scalatore))+'][color='+colorehtml+'][b][font=font/Symbola.ttf]'+unichr(ord(sx[3])+9333)+'[/font][/b][/size][size='+str(int(30*app.scalatore))+']\n'+timesx+'[/color][/size]'
                    else:
                        scoresx_string = '[size='+str(int(45*app.scalatore))+'][color='+colorehtml+'][b][font=font/Symbola.ttf]-[/font][/b][/size][size='+str(int(30*app.scalatore))+']\n'+timesx+'[/color][/size]'
                else:
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
                ICONdx = Button(disabled=False,
                                text=dx[0]+","+dx[3]+","+str(dx[1]),
                                color=[0,0,0,0],
                                size_hint_x=width_icon,
                                background_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_down=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_normal=app.icons_path+app.dictIDicona[dx[0]],
                                background_disabled_down=app.icons_path+app.dictIDicona[dx[0]],
                                border=[0,0,0,0])

                ICONdx.bind(on_press=self.answer_popup)

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


                if self.letterVisibility:
                    if dx[3] != '-':
                        scoredx_string = '[size='+str(int(45*app.scalatore))+'][color='+colorehtml+'][b][font=font/Symbola.ttf]'+unichr(ord(dx[3])+9333)+'[/font][/b][/size][size='+str(int(30*app.scalatore))+']\n'+timedx+'[/color][/size]'
                    else:
                        scoredx_string = '[size='+str(int(45*app.scalatore))+'][color='+colorehtml+'][b][font=font/Symbola.ttf]-[/font][/b][/size][size='+str(int(30*app.scalatore))+']\n'+timedx+'[/color][/size]'
                else:
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

        lBACK = Button(id='back_tmp', text="%s"%(iconfonts.icon('fa-backward')),font_size=50*app.scalatore,bold=True, halign='center', size_hint_x=width_icon, markup=True)
        lBACK.bind(on_press=lambda x : app.load_screen("Question"))
        lSHOW = Button(id='show_tmp', text="%s"%(iconfonts.icon('fa-eye')),font_size=50*app.scalatore,bold=True, halign='center', size_hint_x=width_name, markup=True)
        lSHOW.bind(on_press=lambda x : self.toggleAnswers())
        #bmsx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCsx= Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0], size_hint_x=width_score)

        separation = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_sep)

        bmdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_icon)
        bottomdx = Button(disabled=True, background_disabled_normal='', background_color=[0,0,0,0],size_hint_x=width_name)
        iconBDCdx = IconButton(source='img/logoBdC_bianco.png', size_hint_x=width_score)
        iconBDCdx.bind(on_press=lambda x : app.cmd_line_start())

        g.add_widget(lBACK)
        g.add_widget(lSHOW)
        #g.add_widget(bmsx)
        g.add_widget(iconBDCsx)
        g.add_widget(separation)
        g.add_widget(bmdx)
        g.add_widget(bottomdx)
        g.add_widget(iconBDCdx)
#        g.add_widget(ObjectProperty('back_tmp'),)

        self.add_widget(g)
#        self.add_widget(back_button=ObjectProperty('back_button_tmp'))
        app.score_qst_ready = True

    def answer_popup(self, instance):
        popup_id = instance.text.split(",")[0]
        popup_title = "Risposta di " + str(app.dictIDName[popup_id])
        popup_answer = instance.text.split(",")[1]
        popup_score = int(instance.text.split(",")[2])

        if popup_answer == app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['OK']:
            popup_text = app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['ans'][ord(popup_answer)-65]
            popup_text_2 = '[color=00cc00]%s'%(iconfonts.icon('fa-check-circle'))+'[/color]'
        elif popup_answer == "-":
            popup_text = ""
            popup_text_2 = '[color=ffcc00]%s'%(iconfonts.icon('fa-minus-circle'))+'[/color]'
        else:
            popup_text = app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['ans'][ord(popup_answer)-65]
            popup_text_2 = '[color=ff0000]%s'%(iconfonts.icon('fa-times-circle'))+'[/color]'

        if popup_score > 0:
            popup_color = [0,0.8,0,1]
        elif popup_score == 0:
            popup_color = [1,0.75,0.095,1]
        else:
            popup_color = [0.8,0,0,1]

        if popup_answer != '-':
            popup_content = "[size=100][font=font/Symbola.ttf]" + unichr(ord(popup_answer)+9333) + "[/font][/size]\n[size=40] " + popup_text + " [/size]\n\n" + popup_text_2
        else:
            popup_content = "[size=100][font=font/Symbola.ttf]-[/font][/size]\n[size=40] " + popup_text + " [/size]\n\n" + popup_text_2

        popup = Popup(title=popup_title, title_align='center', title_color=popup_color, title_size='50sp', title_font='font/UbuntuMono-B.ttf', separator_color=popup_color, content=Label(text=popup_content, text_size=(950, None), font_size=80, font_name='font/Ubuntu-L.ttf', halign='center', markup=True),size_hint=(None, None), size=(1000, 800))
        popup.open()

    def toggleAnswers(self):
        self.letterVisibility = not self.letterVisibility
        self.clear_widgets()
        self.buildClassifica(self.sorted_x)
