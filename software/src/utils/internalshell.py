import time
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion


app = App.get_running_app()


class internalShell:

    def __init__(self):
        self.app = app
        self.session = PromptSession(completer=self.InternalCompleter())

    def cmdloop(self):
        print("Shell per attribuzione punti bonus! Digita 'exit' per uscire.")
        print("Per farlo digitare: bonus [last_name] [amount] [hidden]")
        print("Se non digitate hidden si vedrà una finestra che comunica a tutti i punti aggiunti.")
        while True:
            try:
                # Mostra il prompt
                line = self.session.prompt(">>> ")
                # Se digito exit si esce dalla shell
                if line.strip() == "exit":
                    print("Uscita dalla shell.")
                    break
                self.onecmd(line)

            except (KeyboardInterrupt, EOFError):
                print("\nUscita dalla shell.")
                break

    def onecmd(self, line):
        # Analizza e gestisce i comandi
        command, *args = line.split()
        if command == "bonus":
            self.do_bonus(" ".join(args))
        else:
            print(f"Comando sconosciuto: {command}")
    
    class InternalCompleter(Completer):

        def get_completions(self, document, complete_event):
            # Restituisce i completamenti per il comando "bonus"
            text = document.text_before_cursor.lower()

            if text.startswith("bonus "):
                partial_name = text[len("bonus "):]
                completions = [
                    Completion(v.decode('utf-8'), start_position=-len(partial_name))
                    for v in app.dictIDLastName.values()
                    if v.decode('utf-8').startswith(partial_name)
                ]
                yield from completions

    def do_bonus(self, line):
        '''
        bonus [last_name] [amount] ["hidden"] - assegna un bonus alla squadra selezionata
        '''
        try:
            parts = line.split()
            # Utilizzo del comando
            if len(parts) < 2:
                print("<\033[1;91mERROR  \033[0m> Uso: bonus [last_name] [amount] ['hidden']")
                return
            
            
            bonus_team_lastName = parts[0]
    
            # Trasformo tutto in una lista per popter accedere tramite indice all'elemento di interesse.
            # L'utilizzo di decode è dovuto al fatto che all'interno di app.dictIDLastName.values() i nomi
            # sono del tipo: b'nome' quindi in binario.
            id_idx = [v.decode('utf-8') for v in app.dictIDLastName.values()].index(bonus_team_lastName)
            bonus_team_id = list(app.dictIDLastName.keys())[id_idx]
            bonus_amount = int(parts[1])

            # Se parts ha meno di due elementi, allora sarà False
            # Sarà True solo se parts ha più di due elementi e se
            # il terzo è la stringa "hidden"
            bonus_hidden = len(parts) > 2 and parts[2] == "hidden"
            
            if bonus_amount != 0:
                app.GENERAL_SCORE[bonus_team_id] += bonus_amount

                print("<\033[1;92mDONE   \033[0m> bonus to " + str(app.dictIDName[bonus_team_id]) + ": " + str(bonus_amount))

                if not bonus_hidden:

                    if bonus_amount > 0:
                        popup_title = '+' + str(bonus_amount) + ' punti'
                        popup_color = [0,204./255.,0,1]
                    else:
                        popup_title = str(bonus_amount) + ' punti'
                        popup_color = [1,0,0,1]

                    popup_content = "[size=40]SQUADRA[/size]\n\n[b]" + str(app.dictIDName[bonus_team_id].decode('utf-8')) + "[/b]"
                    popup = Popup(title=popup_title, title_align='center', 
                                  title_color=popup_color, title_size='50sp',
                                  title_font='font/UbuntuMono-B.ttf',
                                  separator_color=popup_color,
                                  content=Label(text=popup_content, 
                                  font_size=80, 
                                  font_name='font/UbuntuMono-B.ttf', 
                                  halign='center', 
                                  markup=True),
                                  size_hint=(None, None), 
                                  size=(800, 600))
                    popup.open()

                if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
                    print("<\033[1;93mWARNING\033[0m> score will reset after test section!")
            else:
                print("<\033[1;93mWARNING\033[0m> no bonus given")

        except Exception as e:
            print(f"<\033[1;91mERROR  \033[0m> Errore: {e}")

    
    def do_brightness(self, line):
        'brightness [num_percent] - sets the slave LEDs to num_percent% brightness'
        try:
            num_lum = int(line)
        except:
            print("<\033[1;91mERROR  \033[0m> '" + str(line) + "' isn't a number")
            return False

        if num_lum > 100:
            num_lum = 100
        elif num_lum < 0:
            num_lum = 0

        print("<\033[1;92mDONE   \033[0m> brightness set to " + str(num_lum) + "%")
        if app.no_serial is False:
            app.master.write("lum"+str(num_lum).zfill(3)+"\n")
        else:
            print("<\033[1;91mERROR  \033[0m> serial port not available [no_serial = True]")

    def do_topo(self, line):
        'topo - shows mesh topology'
        if app.no_serial is False:
            app.master.write("topo\n")
            while not app.topologyRead:
                time.sleep(0.05)
            app.topologyRead = False
        else:
            print("<\033[1;91mERROR  \033[0m> serial port not available [no_serial = True]")
