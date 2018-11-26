from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import cmd

app = App.get_running_app()

class internalShell(cmd.Cmd):

    def do_bonus(self, line):
        'bonus [last_name] [amount] ["hidden"] - gives bonus to selected team'
        try:
            bonus_team_lastName = line.split(' ')[0]
            bonus_team_id = app.dictIDLastName.keys()[app.dictIDLastName.values().index(bonus_team_lastName)]
            bonus_amount = int(line.split(' ')[1])
            try:
                bonus_hidden = (line.split(' ')[2] == 'hidden')
            except:
                bonus_hidden = False

            if bonus_amount != 0:
                app.GENERAL_SCORE[bonus_team_id] += bonus_amount

                print "bonus to " + str(app.dictIDName[bonus_team_id]) + ": " + str(bonus_amount)

                if not bonus_hidden:

                    if bonus_amount > 0:
                        popup_title = '+' + str(bonus_amount) + ' punti'
                        popup_color = [0,204./255.,0,1]
                    else:
                        popup_title = str(bonus_amount) + ' punti'
                        popup_color = [1,0,0,1]

                    popup_content = "[size=40]SQUADRA[/size]\n\n[b]" + str(app.dictIDName[bonus_team_id]) + "[/b]"
                    popup = Popup(title=popup_title, title_align='center', title_color=popup_color, title_size='50sp', title_font='font/UbuntuMono-B.ttf', separator_color=popup_color, content=Label(text=popup_content, font_size=80, font_name='font/UbuntuMono-B.ttf', halign='center', markup=True),size_hint=(None, None), size=(800, 600))
                    popup.open()

                if app.SECTIONS[app.SEC_CNT]['type'] == 'test':
                    print "WARNING: score will reset after test section!"
            else:
                print "WARNING: no bonus given"

        except:
            print "ERROR: see help for usage"

    def complete_bonus(self, text, line, begidx, endidx):

        lastNamesOnly = [app.dictIDLastName[key].lower() for key in app.dictIDLastName.keys()]

        if not text:
            completions = lastNamesOnly[:]
        else:
            completions = [f for f in lastNamesOnly if f.startswith(text)]
        return completions

    def do_brightness(self, line):
        'brightness [num_percent] - sets the slave LEDs to num_percent% brightness'
        try:
            num_lum = int(line)
        except:
            print "ERROR: '" + str(line) + "' isn't a number"
            return False

        if num_lum > 100:
            num_lum = 100
        elif num_lum < 0:
            num_lum = 0

        print "brightness set to " + str(num_lum) + "%"
        if app.NOCONTROLLER is False:
            app.master.write("lum"+str(num_lum).zfill(3)+"\n")
        else:
            print "Serial port not available [NOCONTROLLER = True]"

    def do_EOF(self, line):
        'EOF (or ^D) - exits from the shell'
        print "exit"
        return True

    def do_exit(self, line):
        'exit - exits from the shell'
        print "exit"
        return True
