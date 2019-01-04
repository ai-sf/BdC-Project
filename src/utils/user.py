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
    for id in config['Squadre']:
        app.dictIDBonus[id] = int(config.get('Squadre',id).split(',')[0])
        app.dictIDReset[id] = int(config.get('Squadre',id).split(',')[0])
        app.dictIDName[id] = config.get('Squadre',id).split(',')[1].encode('utf-8')
        app.dictIDLastName[id] = config.get('Squadre',id).split(',')[1].split(' ')[1].lower().encode('utf-8')

    app.PositionBefore = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))
    app.Position = dict(zip(app.dictIDName.keys(), [0]*len(app.dictIDName.keys())))
    app.newPositionBefore = False

    app.NUMERO_GIOCATORI = len(app.dictIDName.keys())

    if app.NUMERO_GIOCATORI<16:
        app.sep_name='\n'
    else:
        app.sep_name=' '

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

    app.dictIDicona = { "2142880870": "einstein.png",
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
                        "2486007740": "rutherford.png",
                        "0000000001": "hawking.png",
                        "0000000002": "noether.png",
                        "0000000003": "boltzmann.png",
                        "0000000004": "keplero.png",
                        "0000000005": "copernico.png",
                        "0000000006": "ampere.png",
                        "0000000007": "born.png",
                        "0000000008": "majorana.png",
                        "0000000009": "von neumann.png",
                        "0000000010": "becquerel.png",
                        "0000000011": "bernoulli.png",
                        "0000000012": "pascal.png" }
