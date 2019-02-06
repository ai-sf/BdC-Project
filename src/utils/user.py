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
        try:
            app.dictIDLastName[id] = (config.get('Squadre',id).split(',')[1].split(' ')[1]+'_'+config.get('Squadre',id).split(',')[1].split(' ')[2]).lower().encode('utf-8')
        except:
            app.dictIDLastName[id] = config.get('Squadre',id).split(',')[1].split(' ')[1].lower().encode('utf-8')

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

    app.dictIDicona = { "977148330": "einstein.png",
                        "977144982": "newton.png",
                        "977143789": "planck.png",
                        "977143982": "feynman.png",
                        "977141870": "fermi.png",
                        "977148973": "maxwell.png",
                        "977186140": "schrodinger.png",
                        "977149543": "galileo.png",
                        "981430530": "volta.png",
                        "977151320": "curie.png",
                        "977149772": "heisenberg.png",
                        "977185902": "dirac.png",
                        "981465612": "tesla.png",
                        "981466912": "bohr.png",
                        "977184646": "joule.png",
                        "977186205": "pauli.png",
                        "977143950": "faraday.png",
                        "977185877": "rutherford.png",
                        "977148317": "hawking.png",
                        "977186733": "noether.png",
                        "981413202": "boltzmann.png",
                        "981464356": "keplero.png",
                        "977186685": "copernico.png",
                        "977143946": "ampere.png",
                        "977183543": "born.png",
                        "977149774": "majorana.png",
                        "981466864": "von_neumann.png",
                        "977186485": "becquerel.png",
                        "977183883": "bernoulli.png",
                        "977149683": "pascal.png" }
