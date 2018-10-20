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
    for id in config['Squadre']:
        app.dictIDName[id] = config.get('Squadre',id)

    app.PositionBefore = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))
    app.Position = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))

    app.NUMERO_GIOCATORI = len(app.dictIDName.keys())

    app.FOLDER = config_path + "/" + config.get("Domande","folder")

    app.FIRST_SLIDES = []
    if 'FIRST_SLIDES' in config.sections():
        for id in config['FIRST_SLIDES']:
            slidepath = config_path + "/" + config.get("FIRST_SLIDES", id)
            if os.path.isfile(slidepath):
                app.FIRST_SLIDES.append(slidepath)
            else:
                print("intro slide does not exists at "+slidepath)
                exit()

    # if not os.path.exists(app.FOLDER+'/backup'):
    #     os.makedirs(app.FOLDER+'/backup')

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

    app.NOCONTROLLER = config.getboolean("Partenza", "NOCONTROLLER")

    # if app.BACKUP:
    #      app.starting_counter = backuplist[0]
    #      app.starting_classifica = backuplist[1]
    #      app.astensioni_backup = backuplist[2]
    # else:
    app.starting_counter = 0
    app.starting_classifica = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))

    app.provadomande = config.get("Domande","provadomande")

    app.dictIDicona = { "2142880870" : "einstein.png",
                        "3893145282": "newton.png",
                        "3893136493": "planck.png",
                        "2142879773": "feynman.png",
                        "3893146321": "fermi.png",
                        "2142880227": "maxwell.png",
                        "3893118944": "schrodinger.png",
                        "2142880166": "galileo.png",
                        "3893145819": "volta.png",
                        "2142881769": "curie.png",
                        "3893146227": "heisenberg.png",
                        "2142881923": "dirac.png",
                        "2486007679": "tesla.png",
                        "2486014145": "bohr.png",
                        "2142880856": "joule.png",
                        "2486008734": "pauli.png",
                        "2486014355": "faraday.png",
                        "2486007740": "rutherford.png" }

    app.RANDOM = config.get("Domande","random")

    # localtime = datetime.datetime.now()
    # filenameTime = app.FOLDER+'/backup/stat-'+localtime.strftime('%Y%m%d-%H:%M:%S')+'.dat'
    # fs = open(filenameTime,'w')
    # fs.close()
