from kivy.app import App
import cmd

app = App.get_running_app()

class internalShell(cmd.Cmd):

    #def do_bonus(self, line):
    #    print "bonus to", line

    def do_brightness(self, line):
        'brightness [num_percent] - sets the slave LEDs to num_percent% brightness'
        try:
            num_lum = int(line)
        except:
            print "'" + str(line) + "' isn't a number"
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
