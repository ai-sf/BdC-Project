from kivy.app import App
from random import sample
import os

app = App.get_running_app()

def retriveQuestions():
    for d in app.SECTIONS:
        qst_sec = process(d['path'])
        app.QUESTIONS.append(qst_sec)

    print app.QUESTIONS

def process(filename):

    with open(filename) as f:
        filedomande = f.read().split('\n')

    # absolute question file path
    filepath = os.path.dirname(os.path.realpath(filename))
    app.filepath = filepath

    domande = {}
    for i in range(0,len(filedomande),10):
        print str(i/10)+': '+filedomande[0+i]
        dict = {}
        dict['qst'] = filedomande[0+i]
        Risposte = []
        for j in range(5):
            Risposte.append(filedomande[1+j+i])
        dict['ans'] = Risposte
        dict['OK'] = filedomande[6+i][0]
        if filedomande[7+i].startswith("none"):
            dict['img_bf'] = [app.main_path + "/../" +"logoBdC_bianco.png"]
        else:
            dict['img_bf'] = [filepath + "/" + img for img in filedomande[7+i].split()]
        if filedomande[8+i].startswith("none"):
            dict['img_af'] = [app.main_path + "/" +"logoBdC_bianco.png"]
        else:
            dict['img_af'] = [filepath + "/" + img for img in filedomande[8+i].split()]

        domande[i/10] = dict

    return domande
