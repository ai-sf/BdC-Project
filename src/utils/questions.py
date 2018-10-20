from kivy.app import App
from random import sample
import os

app = App.get_running_app()

def retriveQuestions():
    for d in app.SECTIONS:
        qst_sec = process(d['path'])
        app.QUESTIONS.append(qst_sec)


def process(filename):

    with open(filename) as f:
        filedomande = f.read().split('\n')

    # absolute question file path
    filepath = os.path.dirname(os.path.realpath(filename))
    app.filepath = filepath

    domande = {}
    for i in range(0,len(filedomande),10):
        dict = {}
        dict['qst'] = filedomande[0+i]
        Risposte = []
        for j in range(5):
            Risposte.append(filedomande[1+j+i])
        dict['ans'] = Risposte
        dict['OK'] = filedomande[6+i][0]

        def_img = app.main_path + "/../" +"logoBdC_bianco.png"

        if filedomande[7+i].startswith("none"):
            dict['img_bf'] = [def_img]
        else:
            #dict['img_bf'] = [filepath + "/" + img for img in filedomande[7+i].split()]
            dict['img_bf'] = checkImgEx(filedomande[7+i].split(), def_img)

        if filedomande[8+i].startswith("none"):
            dict['img_af'] = [def_img]
        else:
            #dict['img_af'] = [filepath + "/" + img for img in filedomande[8+i].split()]
            dict['img_af'] = checkImgEx(filedomande[8+i].split(), def_img)

        domande[i/10] = dict

    return domande

def checkImgEx(imglist, default_img):

    newimglist = []
    for img in imglist:
        fname = app.filepath + "/" + img
        if os.path.isfile(fname):
            newimglist.append(fname)
        else:
            newimglist.append(default_img)

    return newimglist
