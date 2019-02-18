from kivy.app import App
from kivy.core.window import Window
import configparser
import os
import datetime
from kivy.properties import DictProperty

app = App.get_running_app()
config = configparser.ConfigParser()

def setGlobal(init_file):

    try:
        config.read(init_file)
    except IOError:
        print('cannot open'+init_file)

    app.port_name = config.get("Partenza", "nome_porta")
    app.scalatore = config.getfloat("Grafica","scalatore")
    app.TOTAL_TIME = config.getint("Partenza", "tempo_risposta")

    app.show_timer = config.getboolean("Partenza", "countdown_domanda")

    config_path = os.path.dirname(os.path.realpath(init_file))

    tmp = 0
    while config.has_section("qst"+str(tmp)):
        section_name = "qst"+str(tmp)

        tmp_dict = {}
        tmp_dict['type'] = config.get(section_name, "type")
        tmp_dict['name'] = config.get(section_name, "name")
        tmp_dict['icon'] = config.get(section_name, "icon")
        tmp_dict['intro'] = config_path + "/" + config.get(section_name, "intro")
        tmp_dict['path'] = config_path + "/" + config.get(section_name, "path")
        tmp_dict['bkg'] = config_path + "/" + config.get(section_name, "bkg")

        app.SECTIONS.append(tmp_dict)
        tmp += 1

    from utils.questions import retriveQuestions
    retriveQuestions()

    app.NUM_OF_QST = len([qst for sublist in app.QUESTIONS for qst in sublist])

    app.dictIDName = {}
    app.dictIDBonus = {}
    app.dictIDReset = {}
    app.dictIDLastName = {}
    app.dictIDicona = {}
    for id in config['Squadre']:
        app.dictIDBonus[id] = int(config.get('Squadre',id).split(',')[0])
        app.dictIDReset[id] = int(config.get('Squadre',id).split(',')[0])
        app.dictIDName[id] = config.get('Squadre',id).split(',')[1].encode('utf-8')
        try:
            app.dictIDLastName[id] = (config.get('Squadre',id).split(',')[1].split(' ')[1]+'_'+config.get('Squadre',id).split(',')[1].split(' ')[2]).lower().encode('utf-8')
        except:
            app.dictIDLastName[id] = config.get('Squadre',id).split(',')[1].split(' ')[1].lower().encode('utf-8')
        app.dictIDicona[id] = app.dictIDLastName[id].decode('utf-8')+".png"

    app.PositionBefore = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))
    app.Position = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))
    app.newPositionBefore = False

    app.NUMERO_GIOCATORI = len(app.dictIDName.keys())

    if app.NUMERO_GIOCATORI<16:
        app.sep_name='\n'
    else:
        app.sep_name=' '

    if app.NUMERO_GIOCATORI<20:
        app.sep_score='\n'
    else:
        app.sep_score='   '


    app.FIRST_SLIDES = []
    if 'FIRST_SLIDES' in config.sections():
        for id in config['FIRST_SLIDES']:
            slidepath = config_path + "/" + config.get("FIRST_SLIDES", id)
            if os.path.isfile(slidepath):
                app.FIRST_SLIDES.append(slidepath)
            else:
                print("intro slide does not exists at "+slidepath)
                exit()

    app.clock_steps = 100

    if config.get("Grafica","fullscreen") == True:
        Window.fullscreen = 'auto'
    else:
        Window.borderless = True
        Window.fullscreen = 1
        screen_width = config.getint("Grafica","width")
        screen_height = config.getint("Grafica","height")
        Window.size = (screen_width, screen_height)

    app.BACKUP = config.getboolean("Partenza","backup")

    app.no_serial = config.getboolean("Partenza", "no_serial")

    app.starting_counter = 0
    app.starting_classifica = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))
